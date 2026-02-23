import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

st.set_page_config(page_title="Financial Data Warehouse", layout="wide")
st.title("📈 Financial Data Warehouse Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
sector = st.sidebar.selectbox("Select Sector", ["All", "Technology", "Finance", "Healthcare", "Energy", "Consumer"])
ticker = st.sidebar.selectbox("Select Ticker", ["AAPL", "MSFT", "NVDA", "JPM", "XOM", "JNJ", "AMZN", "TSLA"])

# Load data
@st.cache_data
def load_data(ticker):
    query = f"""
        SELECT date, ticker, sector, close, daily_return_pct, 
               ma_50, ma_200, rolling_volatility_30d, avg_cpi, avg_fed_rate, ma_cross_signal
        FROM mart_stock_analysis
        WHERE ticker = '{ticker}'
        ORDER BY date
    """
    return pd.read_sql(query, engine)

@st.cache_data
def load_sector_data():
    query = """
        SELECT date, sector,
               avg(daily_return_pct) as avg_return,
               avg(rolling_volatility_30d) as avg_volatility
        FROM mart_stock_analysis
        GROUP BY date, sector
        ORDER BY date
    """
    return pd.read_sql(query, engine)

df = load_data(ticker)
sector_df = load_sector_data()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
latest = df.iloc[-1]
col1.metric("Current Price", f"${latest['close']:.2f}")
col2.metric("Daily Return", f"{latest['daily_return_pct']:.2f}%")
col3.metric("30d Volatility", f"{latest['rolling_volatility_30d']:.2f}")
col4.metric("MA Signal", latest['ma_cross_signal'])

st.divider()

# Price + Moving Averages Chart
st.subheader(f"{ticker} Price vs Moving Averages")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'], y=df['close'], name='Close Price', line=dict(color='white')))
fig.add_trace(go.Scatter(x=df['date'], y=df['ma_50'], name='MA 50', line=dict(color='orange')))
fig.add_trace(go.Scatter(x=df['date'], y=df['ma_200'], name='MA 200', line=dict(color='red')))
fig.update_layout(template='plotly_dark', height=400)
st.plotly_chart(fig, width='stretch')

col1, col2 = st.columns(2)

# Volatility Chart
with col1:
    st.subheader("30-Day Rolling Volatility")
    fig2 = px.line(df, x='date', y='rolling_volatility_30d', template='plotly_dark')
    st.plotly_chart(fig2, width='stretch')

# Macro Context
with col2:
    st.subheader("CPI vs Fed Funds Rate")
    macro_query = """
        SELECT date, indicator, value FROM stg_macro_indicators
        WHERE indicator IN ('CPI', 'fed_funds_rate') ORDER BY date
    """
    macro_df = pd.read_sql(macro_query, engine)
    fig3 = px.line(macro_df, x='date', y='value', color='indicator', template='plotly_dark')
    st.plotly_chart(fig3, width='stretch')

# Sector Performance
st.subheader("Sector Average Daily Returns Over Time")
fig4 = px.line(sector_df, x='date', y='avg_return', color='sector', template='plotly_dark')
st.plotly_chart(fig4, width='stretch')