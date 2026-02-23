# 📈 Financial Data Warehouse

An automated ETL pipeline that ingests daily stock market data and macroeconomic indicators into a PostgreSQL data warehouse, with dbt transformations and a Streamlit dashboard for analysis.

## 🏗️ Architecture
```
Yahoo Finance API → Python ETL → PostgreSQL → dbt → Streamlit Dashboard
FRED API        ↗                           ↗
```

## 🔧 Tech Stack
- **Python** — Data ingestion (yfinance, fredapi)
- **PostgreSQL** — Data warehouse storage
- **dbt** — SQL transformations and data quality tests
- **Streamlit + Plotly** — Interactive dashboard
- **GitHub Actions** — Automated nightly ETL (Mon-Fri at market close)

## 📊 Data Sources
- **30 S&P 500 stocks** across 5 sectors (Technology, Finance, Healthcare, Energy, Consumer)
- **Macroeconomic indicators** — GDP, CPI, Unemployment Rate, Fed Funds Rate, 10yr Treasury (2020–present)

## 🗄️ Data Model (Star Schema)
```
fact_daily_prices
    ├── dim_company (ticker, sector)
    ├── dim_date (date, month, quarter)
    └── dim_macro (GDP, CPI, Fed rate)
```

## 🔄 dbt Pipeline
- **Staging** — Data cleaning, type casting, null filtering
- **Intermediate** — Feature engineering using SQL window functions:
  - 50-day and 200-day moving averages
  - 30-day rolling volatility
  - Daily return percentage
  - 20-day average volume
- **Marts** — Gold layer joining stocks with macro indicators and trading signals (Golden Cross / Death Cross)

## ✅ Data Quality
- 5 dbt tests ensuring no null values in critical columns
- Duplicate prevention on all fact tables

## 📉 Dashboard Features
- Live KPI cards (price, daily return, volatility, MA signal)
- Price vs MA50/MA200 chart
- 30-day rolling volatility over time
- CPI vs Fed Funds Rate macro chart
- Sector average daily returns comparison

## 🚀 Setup
```bash
# Clone the repo
git clone https://github.com/NandanSBharadwaj/financial-data-warehouse.git

# Install dependencies
pip install -r requirements.txt

# Set up .env file
cp .env.example .env
# Add your DB credentials and FRED API key

# Run ingestion
python ingestion/fetch_stocks.py
python ingestion/fetch_macro.py

# Run dbt
cd dbt_project/financial_dw
dbt run
dbt test

# Launch dashboard
streamlit run dashboard/app.py
```

## 📸 Dashboard Preview
![Dashboard](assets/dashboard.png)