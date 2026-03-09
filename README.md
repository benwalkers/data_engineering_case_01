# data_engineering_case_01
GCP Data Engineering Solution for a click streaming business model

In-scope raw assets
XYZ-benjaminpiscoya.XYZ.modules
XYZ-benjaminpiscoya.XYZ.module_Services

This document explains the challenge, the target design, the rationale for keeping DQ in BigQuery, and the specific session_id privacy treatment.
Executive summary

This XYZ case is as a governed streaming data product rather than as a simple SQL cleansing exercise. The raw event tables are large, continuously growing and carry both business-quality defects and privacy concerns.
The recommended target architecture uses Pub/Sub and Dataflow for unbounded ingestion, applies Sensitive Data Protection specifically to session_id before curated exposure, lands trusted and rejected records in BigQuery, and uses Dataplex to scan and govern the landed assets.
A BigQuery DQ zone is intentionally part of the design because failed records are still operational evidence. They must remain queryable for trend analysis, root-cause analysis, producer feedback and replay selection. Cloud Storage remains useful only as the optional cold archive of the untouched reject payload.

1. Problem definition
XYZ captures behavioural interaction events from retailer experiences where product content modules are shown to end users. These events power downstream content analytics, client reporting, and marketing insight.
The raw layer is large and continuously growing. In previous exploration, the two principal raw tables in scope were XYZ-benjaminpiscoya.XYZ.modules and XYZ-benjaminpiscoya.XYZ.module_Services. The target solution therefore needs to support unbounded ingestion rather than a one-off batch clean-up.
The case also contains a specific privacy requirement: session_id is a field that should not be exposed raw in curated analytical outputs.

2. Raw assets and schema access
The exact schema should be surfaced from BigQuery INFORMATION_SCHEMA rather than copied manually into a design document. That keeps the report accurate even if the source schema evolves.
The architecture below therefore uses a selected schema view: only fields that materially affect the design are highlighted.
Recommended schema access SQL
SELECT table_name, row_count
FROM `XYZ-benjaminpiscoya.XYZ.__TABLES__`;
SELECT table_name, column_name, data_type
FROM `XYZ-benjaminpiscoya.XYZ.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN ('modules', 'module_Services')
ORDER BY table_name, ordinal_position;

