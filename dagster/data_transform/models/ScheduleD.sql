{{ config(
    materialized='incremental',
    incremental_strategy='insert_overwrite',
    partition_by='YearMonth'
) }}

SELECT 
    *
FROM {{ source("staging", "STG_ScheduleD") }}
{% if is_incremental() %}
WHERE YearMonth = '{{ var("yearmonth") }}'
{% endif %}