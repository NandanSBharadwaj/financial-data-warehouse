with stock as (
    select * from {{ ref('stg_stock_prices') }}
)

select
    date,
    ticker,
    sector,
    close,
    volume,

    -- Moving Averages
    round(avg(close) over (
        partition by ticker order by date
        rows between 49 preceding and current row
    ), 2) as ma_50,

    round(avg(close) over (
        partition by ticker order by date
        rows between 199 preceding and current row
    ), 2) as ma_200,

    -- 30-day Rolling Volatility (std dev of daily returns)
    round(stddev(close) over (
        partition by ticker order by date
        rows between 29 preceding and current row
    ), 4) as rolling_volatility_30d,

    -- Daily Return
    round((close - lag(close) over (partition by ticker order by date)) 
        / nullif(lag(close) over (partition by ticker order by date), 0) * 100, 4) as daily_return_pct,

    -- Volume vs 20-day average volume
    round(avg(volume) over (
        partition by ticker order by date
        rows between 19 preceding and current row
    ), 0) as avg_volume_20d

from stock