import os

# --- DB Connection Params ---
DB_PARAMS = {
    "host": "192.168.56.10",
    "database": "asc_videogames_db",  # Change to asc_videogames_db if applicable
    "user": "postgres",
    "password": "@Suricat0s2o26",
    "port": 5432
}

# --- CheapShark API Config. ---
CHEAPSHARK_BASE_URL = "https://cheapshark.com/api/1.0"

# Customizable search filters for the API request
CHEAPSHARK_FILTERS = {
    "storeID": "1",          # 1 represents Steam (can be comma-separated list)
    "upperPrice": "50",      # Maximum price filter
    "lowerPrice": "0",       # Minimum price filter
    "sortBy": "Savings",     # Sort deals by discount percentage
    "pageSize": "60"         # Max number permitted of deal records to fetch per page
}

# Global accumulation target boundary
TOTAL_DEALS_TARGET = 300


# --- Web Server Directory Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "base.html")
CSS_SOURCE = os.path.join(BASE_DIR, "templates", "assets", "css", "styles.css")

APACHE_DIR = "/var/www/html"
APACHE_CSS_DIR = os.path.join(APACHE_DIR, "assets", "css")