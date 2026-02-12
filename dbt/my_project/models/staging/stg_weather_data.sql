{{ config(
    materialized='table',
    unique_key='id'
)
}}

with source as (
    select *
    from {{ source('dev','raw_weather_data')}}
),

de_dup as (
    select 
        *,
        row_number() over (partition by time order by inserted_at) as rn 
    from source
)

select 
    id,
    city,
    temperature,
    weather_descriptions,
    wind_speed,
    time as weather_time_local,
    inserted_at AT TIME ZONE 'UTC' AT TIME ZONE timezone AS inserted_at_local,
    timezone
from  de_dup
where rn=1
