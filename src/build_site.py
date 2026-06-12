import os
import json
import shutil
from config import TEMPLATE_PATH, CSS_SOURCE, APACHE_DIR, APACHE_CSS_DIR
from db_context import DatabaseConnection, handle_errors

class StaticSiteGenerator:
    def __init__(self):
        # We no longer need a brittle DOM placeholder string
        pass

    @handle_errors
    def get_deals_from_db(self):
        """Fetches unified relational information for the storefront catalog."""
        query = """
            SELECT g.title, g.background_image, g.rating, d.price, d.retail_price, d.savings, 
                   d.purchase_url, s.name
            FROM Game g
            JOIN Deal d ON g.game_id = d.game_id
            JOIN Store s ON d.store_id = s.store_id;
        """
        with DatabaseConnection() as cur:
            cur.execute(query)
            records = cur.fetchall()
    
            dataset = []
            for row in records:
                dataset.append({
                    "title": row[0],
                    "image": row[1],
                    "rating": float(row[2]) if row[2] else 0.0,
                    "price": float(row[3]),
                    "retail_price": float(row[4]),
                    "savings": float(row[5]),
                    "url": row[6],
                    "store_name": row[7]
                })
            return dataset

    @handle_errors
    def compile(self):
        """Compiles raw relational rows into an optimized external asset architecture."""
        print("Initiating pipeline compilation of structural web production assets...")
        deals_list = self.get_deals_from_db()
        
        if not deals_list:
            print("⚠️ Production query returns an empty dataset. Halting compilation.")
            return

        # Ensure directory roots exist inside our web server target destination
        os.makedirs(os.path.join(APACHE_DIR, "assets", "data"), exist_ok=True)
        os.makedirs(APACHE_CSS_DIR, exist_ok=True)

        # Optimization: Dump data to a distinct, highly-cacheable JSON asset target
        data_target_path = os.path.join(APACHE_DIR, "assets", "data", "deals.json")
        with open(data_target_path, "w", encoding="utf-8") as data_file:
            json.dump(deals_list, data_file, check_circular=False, separators=(',', ':'))

        if not os.path.exists(TEMPLATE_PATH):
            raise FileNotFoundError(f"Development layout configuration missing at target: {TEMPLATE_PATH}")

        # Copy your structural base template completely untouched as index.html
        shutil.copy(TEMPLATE_PATH, os.path.join(APACHE_DIR, "index.html"))

        if os.path.exists(CSS_SOURCE):
            shutil.copy(CSS_SOURCE, os.path.join(APACHE_CSS_DIR, "styles.css"))
            print("CSS production layout variables successfully synchronized.")

        print("🚀 Compiling completed! Apache deployment successfully executed.")

if __name__ == "__main__":
    generator = StaticSiteGenerator()
    generator.compile()