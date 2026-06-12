import psycopg2
import sys
from functools import wraps
from config import DB_PARAMS

def handle_errors(func):
    """Decorator to centralize error handling and exception logging."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except psycopg2.Error as db_err:
            print(f"❌ Database Error in '{func.__name__}': {db_err}", file=sys.stderr)
        except Exception as e:
            print(f"❌ Unexpected Error in '{func.__name__}': {e}", file=sys.stderr)
    return wrapper

class DatabaseConnection:
    """Context manager utilizing magic methods for secure connection management."""
    def __enter__(self):
        self.conn = psycopg2.connect(**DB_PARAMS)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
            print("🔄 Transaction rolled back due to an unhandled exception.")
        else:
            self.conn.commit()
        self.cur.close()
        self.conn.close()
