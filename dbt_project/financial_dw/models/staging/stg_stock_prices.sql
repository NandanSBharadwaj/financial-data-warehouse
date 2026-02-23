with source as (
    select * from raw_stock_prices
)

select
    date::date as date,
    ticker,
    sector,
    open::numeric,
    high::numeric,
    low::numeric,
    close::numeric,
    volume,
    round(((close::numeric - low::numeric) / nullif((high::numeric - low::numeric), 0) * 100), 2) as daily_range_pct
from source
where close is not null