#!/usr/bin/env python3
"""
fetch_data.py | Dual-API Data Ingestion Pipeline
Consumes RAWG (metadata) & CheapShark (pricing) -> Upserts into PostgreSQL
"""

import os
import time
import logging
import requests
import psycopg2

# ================= CONFIGURATION =================
DB_HOST = os.getenv("DB_HOST", "192.168.56.10")
DB_NAME = os.getenv("DB_NAME", "asc_videogames_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
RAWG_API_KEY = os.getenv("RAWG_API_KEY", "RAWG_API_KEY")

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def run_pipeline():
    if not DB_PASS:
        raise SystemExit("❌ ERROR: DB_PASS environment variable not set. Export it before running.")
        
    logging.info("🔌 Connecting to PostgreSQL...")
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    
    try:
        # 1. Pre-cache Store metadata from CheapShark
        logging.info("📦 Fetching store list...")
        stores = requests.get("https://www.cheapshark.com/api/1.0/stores").json()
        for s in stores:
            cur.execute("""INSERT INTO Store (store_id, name, base_url) 
                           VALUES (%s, %s, %s) ON CONFLICT (store_id) DO NOTHING""",
                        (int(s["storeID"]), s["storeName"], "https://www.cheapshark.com/"))

        # 2. Fetch RAWG Games (Top rated)
        url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&page_size=15&ordering=-rating"
        rawg_games = requests.get(url).json().get("results", [])
        logging.info(f"🎮 Fetched {len(rawg_games)} games from RAWG.")

        # 3. Process & Cross-reference
        for game in rawg_games:
            time.sleep(0.5)  # Rate limit respect
            title = game.get("name", "Unknown")
            
            # CheapShark price lookup
            cs_res = requests.get("https://www.cheapshark.com/api/1.0/deals", 
                                  params={"title": title, "limit": 1, "sortBy": "Savings"}).json()
            deal = cs_res[0] if cs_res else None
            
            if not deal:
                continue  # Skip games without active deals

            # Upsert Genres
            for genre in game.get("genres", []):
                cur.execute("""INSERT INTO Genre (genre_id, name, slug) 
                               VALUES (%s, %s, %s) ON CONFLICT (genre_id) DO NOTHING""",
                            (genre["id"], genre["name"], genre.get("slug", "")))

            # Upsert Game & Retrieve ID
            cur.execute("""INSERT INTO Game (title, description, release_date, rating, background_image)
                           VALUES (%s, %s, %s, %s, %s) ON CONFLICT (title) DO NOTHING RETURNING game_id""",
                        (title, game.get("description_raw"), game.get("released"), 
                         game.get("rating"), game.get("background_image")))
            
            result = cur.fetchone()
            gid = result[0] if result else cur.execute("SELECT game_id FROM Game WHERE title=%s", (title,)) or cur.fetchone()[0]

            # Upsert Genre Mapping
            for genre in game.get("genres", []):
                cur.execute("""INSERT INTO Game_Genre (game_id, genre_id) 
                               VALUES (%s, %s) ON CONFLICT DO NOTHING""", (gid, genre["id"]))

            # Upsert Deal (UPDATE on price change)
            cur.execute("""INSERT INTO Deal (deal_id, game_id, store_id, price, retail_price, savings, purchase_url)
                           VALUES (%s, %s, %s, %s, %s, %s, %s) 
                           ON CONFLICT (deal_id) DO UPDATE 
                           SET price = EXCLUDED.price, retail_price = EXCLUDED.retail_price, 
                               savings = EXCLUDED.savings, purchase_url = EXCLUDED.purchase_url""",
                        (deal["dealID"], gid, int(deal["storeID"]), float(deal["salePrice"]), 
                         float(deal["normalPrice"]), float(deal["savings"]),
                         f"https://www.cheapshark.com/redirect?dealID={deal['dealID']}"))
            
            conn.commit()
            logging.info(f"[✅] {title} | ${deal['salePrice']} | -{deal['savings']}% OFF")

    except Exception as e:
        conn.rollback()
        logging.error(f"[❌] Transaction rolled back: {e}")
    finally:
        cur.close()
        conn.close()
        logging.info("🏁 Ingestion pipeline completed.")

if __name__ == "__main__":
    run_pipeline()
