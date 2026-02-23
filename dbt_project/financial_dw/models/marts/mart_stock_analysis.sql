with stock as (
    select * from {{ ref('int_stock_features') }}
),

macro as (
    select * from {{ ref('stg_macro_indicators') }}
),

cpi as (
    select date_trunc('month', date) as month, avg(value) as avg_cpi
    from macro
    where indicator = 'CPI'
    group by 1
),

fed as (
    select date_trunc('month', date) as month, avg(value) as avg_fed_rate
    from macro
    where indicator = 'fed_funds_rate'
    group by 1
)

select
    s.date,
    s.ticker,
    s.sector,
    s.close,
    s.daily_return_pct,
    s.ma_50,
    s.ma_200,
    s.rolling_volatility_30d,
    s.avg_volume_20d,

    -- Macro context
    c.avg_cpi,
    f.avg_fed_rate,

    -- Signal: is stock above 50-day MA?
    case when s.close > s.ma_50 then 'Above MA50' else 'Below MA50' end as ma50_signal,

    -- Signal: golden cross (50MA > 200MA)
    case when s.ma_50 > s.ma_200 then 'Golden Cross' else 'Death Cross' end as ma_cross_signal

from stock s
left join cpi c on date_trunc('month', s.date) = c.month
left join fed f on date_trunc('month', s.date) = f.month