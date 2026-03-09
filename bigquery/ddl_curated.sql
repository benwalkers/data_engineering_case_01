CREATE SCHEMA IF NOT EXISTS `flixmedia_curated`;

CREATE TABLE IF NOT EXISTS `flixmedia_curated.modules_curated`
(
  date DATE,
  session_token STRING,
  distributor_id INT64,
  product_id INT64,
  module_id STRING,
  module_pos INT64,
  views INT64,
  clicks INT64,
  view_time INT64,
  dq_flags ARRAY<STRING>,
  processed_ts TIMESTAMP
)
PARTITION BY date
CLUSTER BY distributor_id, product_id;

CREATE TABLE IF NOT EXISTS `flixmedia_curated.module_services_curated`
(
  date DATE,
  session_token STRING,
  distributor_id INT64,
  product_id INT64,
  service STRING,
  service_type STRING,
  lang STRING,
  currency STRING,
  gbp_price FLOAT64,
  dq_flags ARRAY<STRING>,
  processed_ts TIMESTAMP
)
PARTITION BY date
CLUSTER BY distributor_id, product_id;
