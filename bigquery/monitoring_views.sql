CREATE OR REPLACE VIEW `xyz_dq.v_modules_dq_summary` AS
SELECT
  date,
  severity,
  flag AS dq_flag,
  COUNT(*) AS dq_rows
FROM `xyz_dq.modules_dq`,
UNNEST(dq_flags) AS flag
GROUP BY 1,2,3;

CREATE OR REPLACE VIEW `xyz_dq.v_module_services_dq_summary` AS
SELECT
  date,
  severity,
  flag AS dq_flag,
  COUNT(*) AS dq_rows
FROM `xyz_dq.module_services_dq`,
UNNEST(dq_flags) AS flag
GROUP BY 1,2,3;
