# src/cleaner.py
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cleaner")

RAW_PATH = "data/raw.json"
CLEANED_PATH = "data/cleaned.json"

def load_raw_data(path=RAW_PATH) -> pd.DataFrame:
    """Load raw JSON data into pandas DataFrame"""
    df = pd.read_json(path)
    logger.info(f"Loaded {len(df)} raw items")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the data"""
    # --- Remove duplicates based on URL ---
    df = df.drop_duplicates(subset="url")

    # --- Strip text fields ---
    df["name"] = df["name"].astype(str).str.strip().str.title()
    df["sku"] = df["sku"].astype(str).str.strip()
    df["image"] = df["image"].astype(str).str.strip()

    # --- Convert price to numeric ---
    df["price"] = df["price"].astype(str).str.replace("₸", "").str.replace(" ", "").str.strip()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")  # некорректные значения станут NaN

    logger.info(f"Cleaned data contains {len(df)} items")
    return df

def save_cleaned_data(df: pd.DataFrame, path=CLEANED_PATH):
    df.to_json(path, orient="records", force_ascii=False, indent=2)
    logger.info(f"Saved cleaned data to {path}")

if __name__ == "__main__":
    df_raw = load_raw_data()
    df_cleaned = clean_data(df_raw)
    save_cleaned_data(df_cleaned)
