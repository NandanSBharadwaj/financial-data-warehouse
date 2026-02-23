with source as (
    select * from raw_macro_indicators
)

select
    date::date as date,
    indicator,
    round(value::numeric, 4) as value
from source
where value is not null