{{ config(
    materialized='incremental',
    incremental_strategy='insert_overwrite',
    partition_by='YearMonth'
) }}

SELECT * FROM (
    SELECT ReportId , 'ScheduleA' AS ScheduleType, ScheduleAId AS ScheduleId, YearMonth
    FROM {{ ref('ScheduleA') }} sa 
    UNION ALL 
    SELECT ReportId , 'ScheduleB' AS ScheduleType , ScheduleBId AS ScheduleId,  YearMonth
    FROM {{ ref('ScheduleB') }} sb 
    UNION ALL 
    SELECT ReportId , 'ScheduleC' AS ScheduleType , ScheduleCId AS ScheduleId,  YearMonth
    FROM {{ ref('ScheduleC') }} sc 
    UNION ALL 
    SELECT ReportId , 'ScheduleD' AS ScheduleType , ScheduleDId AS ScheduleId,  YearMonth
    FROM {{ ref('ScheduleD') }} sc 
    UNION ALL 
    SELECT ReportId , 'ScheduleE' AS ScheduleType , ScheduleEId AS ScheduleId,  YearMonth
    FROM {{ ref('ScheduleE') }} sc 
    UNION ALL 
    SELECT ReportId , 'ScheduleF' AS ScheduleType , ScheduleFId AS ScheduleId,  YearMonth
    FROM {{ ref('ScheduleF') }} sc 
    UNION ALL 
    SELECT ReportId , 'ScheduleG' AS ScheduleType , ScheduleGId AS ScheduleId,  YearMonth
    FROM {{ ref('ScheduleG') }} sc 
    UNION ALL 
    SELECT ReportId , 'ScheduleH' AS ScheduleType , ScheduleHId AS ScheduleId,  YearMonth
    FROM {{ ref('ScheduleH') }} sc 
    UNION ALL 
    SELECT ReportId , 'ScheduleI' AS ScheduleType , ScheduleIId AS ScheduleId,  YearMonth
    FROM {{ ref('ScheduleI') }} sc 
)
{% if is_incremental() %}
WHERE YearMonth = '{{ var("yearmonth") }}'
{% endif %}