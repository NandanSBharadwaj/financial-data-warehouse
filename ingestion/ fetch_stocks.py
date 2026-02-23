import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 30 S&P 500 stocks across 5 sectors
TICKERS = {
    "Technology": ["AAPL", "MSFT", "NVDA", "GOOGL", "META"],
    "Finance": ["JPM", "BAC", "GS", "MS", "WFC"],
    "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "MRK"],
    "Energy": ["XOM", "CVX", "COP", "SLB", "EOG"],
    "Consumer": ["AMZN", "TSLA", "HD", "MCD", "NKE"]
}

def fetch_stock_data():
    all_data = []

    for sector, tickers in TICKERS.items():
        for ticker in tickers:
            print(f"Fetching {ticker} ({sector})...")
            df = yf.download(ticker, start="2020-01-01", auto_adjust=True)
            df = df.reset_index()
            
            # Flatten MultiIndex columns if present
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0].lower() if col[1] == '' else col[0].lower() for col in df.columns]
            else:
                df.columns = [col.lower() for col in df.columns]
            
            df["ticker"] = ticker
            df["sector"] = sector
            all_data.append(df)

    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.rename(columns={"date": "date", "open": "open", "high": "high",
                                         "low": "low", "close": "close", "volume": "volume"})
    combined = combined[["date", "ticker", "sector", "open", "high", "low", "close", "volume"]]
    combined.to_sql("raw_stock_prices", engine, if_exists="replace", index=False)
    print(f"✅ Loaded {len(combined)} rows into raw_stock_prices")

if __name__ == "__main__":
    fetch_stock_data()