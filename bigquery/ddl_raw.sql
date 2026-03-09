CREATE SCHEMA IF NOT EXISTS `xyz_raw`;

CREATE TABLE IF NOT EXISTS `xyz_raw.modules_raw`
(
  ingest_ts TIMESTAMP NOT NULL,
  source_system STRING,
  payload_json JSON
)
PARTITION BY DATE(ingest_ts);

CREATE TABLE IF NOT EXISTS `xyz_raw.module_services_raw`
(
  ingest_ts TIMESTAMP NOT NULL,
  source_system STRING,
  payload_json JSON
)
PARTITION BY DATE(ingest_ts);
