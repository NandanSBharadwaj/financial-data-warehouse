import pandas as pd
from fredapi import Fred
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
fred = Fred(api_key=FRED_API_KEY)

# Key macro indicators
INDICATORS = {
    "GDP": "GDP",
    "CPI": "CPIAUCSL",
    "unemployment_rate": "UNRATE",
    "fed_funds_rate": "FEDFUNDS",
    "10yr_treasury": "DGS10"
}

def fetch_macro_data():
    all_data = []

    for name, series_id in INDICATORS.items():
        print(f"Fetching {name}...")
        series = fred.get_series(series_id, observation_start="2020-01-01")
        df = series.reset_index()
        df.columns = ["date", "value"]
        df["indicator"] = name
        all_data.append(df)

    combined = pd.concat(all_data, ignore_index=True)
    combined.to_sql("raw_macro_indicators", engine, if_exists="replace", index=False)
    print(f"✅ Loaded {len(combined)} rows into raw_macro_indicators")

if __name__ == "__main__":
    fetch_macro_data()