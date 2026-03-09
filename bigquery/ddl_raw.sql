CREATE SCHEMA IF NOT EXISTS `flixmedia_raw`;

CREATE TABLE IF NOT EXISTS `flixmedia_raw.modules_raw`
(
  ingest_ts TIMESTAMP NOT NULL,
  source_system STRING,
  payload_json JSON
)
PARTITION BY DATE(ingest_ts);

CREATE TABLE IF NOT EXISTS `flixmedia_raw.module_services_raw`
(
  ingest_ts TIMESTAMP NOT NULL,
  source_system STRING,
  payload_json JSON
)
PARTITION BY DATE(ingest_ts);
