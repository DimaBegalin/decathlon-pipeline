# src/loader.py
import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("loader")

CLEANED_PATH = "data/cleaned.json"
DB_PATH = "data/output.db"
TABLE_NAME = "products"

def load_cleaned_data(path=CLEANED_PATH) -> pd.DataFrame:
    """Load cleaned JSON data into DataFrame"""
    df = pd.read_json(path)
    logger.info(f"Loaded {len(df)} cleaned items")
    return df

def save_to_sqlite(df: pd.DataFrame, db_path=DB_PATH, table_name=TABLE_NAME):
    """Save DataFrame to SQLite database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # --- Создаем таблицу ---
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            url TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            sku TEXT,
            image TEXT
        )
    """)
    conn.commit()

    # --- Загружаем данные через pandas ---
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    logger.info(f"Saved {len(df)} items to SQLite database '{db_path}' in table '{table_name}'")

    conn.close()

if __name__ == "__main__":
    df_cleaned = load_cleaned_data()
    save_to_sqlite(df_cleaned)
