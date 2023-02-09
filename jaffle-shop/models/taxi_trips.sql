{{ config(materialized='view') }}
select * from bigquery-public-data.chicago_taxi_trips.taxi_trips
