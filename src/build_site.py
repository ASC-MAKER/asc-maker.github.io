#!/usr/bin/env python3
"""
build_site.py | Static Site Generator (SSG) + External Asset Sync
Fetches aggregated DB data -> Renders index.html -> Deploys to Apache vHost
"""

import os
import shutil
import psycopg2
import logging
from pathlib import Path

# ================= CONFIGURATION =================
DB_HOST = os.getenv("DB_HOST", "192.168.56.10")
DB_NAME = os.getenv("DB_NAME", "asc_videogames_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")

# Absolute paths for reliability
BASE_DIR = Path("/home/project-web/asc-videogames")
TEMPLATE_DIR = BASE_DIR / "templates"
PUBLIC_DIR = Path("/var/www/asc-videogames/public")
ASSETS_SRC = TEMPLATE_DIR / "assets"
ASSETS_DEST = PUBLIC_DIR / "assets"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def sync_assets():
    """Copies static assets (CSS/IMG) to Apache public dir."""
    if ASSETS_SRC.exists():
        shutil.copytree(ASSETS_SRC, ASSETS_DEST, dirs_exist_ok=True)
        logging.info("📦 Static assets synced to /var/www/.../public/assets/")

def build_site():
    if not DB_PASS:
        raise SystemExit("❌ ERROR: DB_PASS environment variable not set.")
        
    logging.info("🔌 Connecting to PostgreSQL for SSG query...")
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()

    # Optimized aggregation query
    QUERY = """
    SELECT g.title, g.background_image, g.rating, 
           d.price, d.retail_price, d.savings, d.purchase_url,
           s.name AS store_name
    FROM Deal d
    JOIN Game g ON d.game_id = g.game_id
    JOIN Store s ON d.store_id = s.store_id
    WHERE d.savings > 0
    ORDER BY d.savings DESC
    LIMIT 40;
    """
    
    try:
        cur.execute(QUERY)
        rows = cur.fetchall()
        
        if not rows:
            logging.warning("⚠️ No deals found in DB. Check fetch_data.py execution.")
            return

        # Generate HTML Cards
        cards_html = ""
        for row in rows:
            title, bg, rating, price, retail, savings, url, store = row
            retail = retail if retail and retail > 0 else price * 1.2
            img = bg or "https://via.placeholder.com/640x360?text=No+Image"
            
            cards_html += f"""
            <article class="game-card">
                <div class="card-image" style="background-image: url('{img}');"></div>
                <div class="card-content">
                    <h2 class="game-title">{title}</h2>
                    <div class="meta-row">
                        <span class="rating">⭐ {rating or 'N/A'}</span>
                        <span class="store-badge">{store}</span>
                    </div>
                    <div class="price-block">
                        <span class="price-old">${retail:.2f}</span>
                        <span class="price-new">${price:.2f}</span>
                        <span class="discount-tag">-{savings:.0f}% OFF</span>
                    </div>
                    <a href="{url}" target="_blank" rel="noopener" class="buy-btn">🛒 Buy Deal</a>
                </div>
            </article>"""

        # Render Template
        template_path = TEMPLATE_DIR / "base.html"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
            
        html_template = template_path.read_text()
        final_html = html_template.replace("<!-- GAMES_CONTAINER -->", cards_html)
        
        # Ensure public dir & write output
        PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
        (PUBLIC_DIR / "index.html").write_text(final_html)
        logging.info(f"🌐 Site successfully built at {PUBLIC_DIR / 'index.html'}")

        # Execute asset bundling step
        sync_assets()

    except Exception as e:
        logging.error(f"[❌] Build failed: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    build_site()
