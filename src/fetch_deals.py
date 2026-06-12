import requests
import psycopg2
from config import DB_PARAMS, CHEAPSHARK_BASE_URL, CHEAPSHARK_FILTERS, TOTAL_DEALS_TARGET

class CheapSharkImporter:
    def __init__(self):
        # Correctly builds endpoints using standard parameters
        self.deals_url = f"{CHEAPSHARK_BASE_URL}/deals"
        self.stores_url = f"{CHEAPSHARK_BASE_URL}/stores"

    def sync_stores(self):
        """Fetches and inserts/updates active storefronts from CheapShark API."""
        print("🏪 Syncing store directory...")
        response = requests.get(self.stores_url)
        response.raise_for_status()
        stores = response.json()

        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                for store in stores:
                    if store.get("isActive") == 1:
                        query = """
                            INSERT INTO Store (store_id, name, base_url)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (store_id) DO UPDATE \
                            SET name = EXCLUDED.name;
                        """
                        base_url = f"https://cheapshark.com{store['storeID']}"
                        cur.execute(query, (int(store["storeID"]), store["storeName"], base_url))
        print("✅ Store directory sync completed.")

    def fetch_and_save_deals(self):
        """Queries active deals from API using multi-page iteration logic and populates tables."""
        print(f"🚀 Initializing multi-page loop target: {TOTAL_DEALS_TARGET} deals...")
        
        all_deals = []
        current_page = 0
        page_size = int(CHEAPSHARK_FILTERS.get("pageSize", 60))
        
        # Create an isolated local copy of filters to avoid global state pollution
        api_parameters = CHEAPSHARK_FILTERS.copy()
        
        # Paginate sequentially until collection targets are met
        while len(all_deals) < TOTAL_DEALS_TARGET:
            api_parameters["pageNumber"] = current_page
            print(f"📥 Querying API page indices: [Page {current_page}] (Current total: {len(all_deals)})...")
            
            response = requests.get(self.deals_url, params=api_parameters)
            response.raise_for_status()
            page_payload = response.json()
            
            if not page_payload:
                print("🏁 API reported end of catalog stream early. Breaking pagination loop.")
                break
                
            all_deals.extend(page_payload)
            current_page += 1
            
            # Defensive break: if we receive fewer items than the requested page size, no more remain
            if len(page_payload) < page_size:
                break

        # Constrain exactly to our config boundary definitions
        all_deals = all_deals[:TOTAL_DEALS_TARGET]
        print(f"📦 Successfully collected {len(all_deals)} raw records from endpoint pools.")

        if not all_deals:
            return

        # --- HIGH-PERFORMANCE IN-MEMORY RECORD PIPELINE ---
        # Fetching titles ahead of time avoids running 300 sequential SELECT queries
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                print("⚡ Building look-up relational game index cache...")
                cur.execute("SELECT title, game_id FROM Game;")
                game_cache = {row[0]: row[1] for row in cur.fetchall()}
                
                print("💾 Compiling data maps into PostgreSQL storage context partitions...")
                for item in all_deals:
                    title = item["title"]
                    
                    if title in game_cache:
                        game_id = game_cache[title]
                    else:
                        # Insert new unique item structures cleanly
                        game_query = """
                            INSERT INTO Game (title, background_image, rating)
                            VALUES (%s, %s, %s)
                            RETURNING game_id;
                        """
                        rating_score = float(item.get("dealRating", 0.0))
                        cur.execute(game_query, (title, item["thumb"], rating_score))
                        game_id = cur.fetchone()[0]
                        # Dynamically append back into cache to capture repeating titles within the identical payload stream
                        game_cache[title] = game_id

                    # Handle Deal Insertion or Updates with optimized structural upsert syntax
                    deal_query = """
                        INSERT INTO Deal (deal_id, game_id, store_id, price, retail_price, savings, purchase_url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (deal_id) DO UPDATE SET
                            price = EXCLUDED.price,
                            savings = EXCLUDED.savings;
                    """
                    purchase_url = f"https://www.cheapshark.com/redirect?dealID={item['dealID']}"
                    cur.execute(deal_query, (
                        item["dealID"],
                        game_id,
                        int(item["storeID"]),
                        float(item["salePrice"]),
                        float(item["normalPrice"]),
                        float(item["savings"]),
                        purchase_url
                    ))
                    
        print(f"✅ Data injection complete. {len(all_deals)} deals successfully recorded and cached.")

if __name__ == "__main__":
    importer = CheapSharkImporter()
    importer.sync_stores()
    importer.fetch_and_save_deals()