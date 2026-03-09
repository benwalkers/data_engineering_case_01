# XYZ Architecture Report

## Problem definition

XYZ receives high-volume retailer interaction events for product content modules. The main raw analytical inputs are:

- `xyz-benjaminpiscoya.xyz.modules`
- `xyz-benjaminpiscoya.xyz.module_Services`

The proposed target state addresses unbounded ingestion, data quality, governance, and protection of `session_id`.

### Example raw access queries

```sql
SELECT *
FROM `xyz-benjaminpiscoya.xyz.modules`
LIMIT 100;
```

```sql
SELECT column_name, data_type
FROM `xyz-benjaminpiscoya.xyz.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'modules';
```

## Target architecture

- Retailer trackers publish to Pub/Sub.
- Dataflow validates schema and business rules.
- `session_id` is tokenised before curated and DQ persistence.
- Valid rows land in BigQuery curated.
- Invalid rows land in BigQuery DQ.
- Optional sanitised failed-event snapshots land in Cloud Storage archive.
- Contracts are versioned in Git and deployed through Composer / CI.
- Dataplex runs governed post-ingestion scans on BigQuery assets.

## Why BigQuery DQ

BigQuery DQ is the primary operational DQ layer because it supports SQL-based observability, dashboards, root-cause analysis, and reprocessing selection. Cloud Storage is optional archive storage, not the analytical DQ system of record.
