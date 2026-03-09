from __future__ import annotations
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

REPO_ROOT = "/opt/airflow/dags/repo/data_engineering_case"

with DAG(
    dag_id="XYZ_contract_deploy",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["flixmedia", "contracts"],
) as dag:
    validate_contracts = BashOperator(
        task_id="validate_contracts",
        bash_command=f"python {REPO_ROOT}/validation/validate_contracts.py --contracts-dir {REPO_ROOT}/contracts",
    )
    deploy_notice = BashOperator(
        task_id="deploy_notice",
        bash_command="echo 'Contracts validated. Add deployment task here.'",
    )
    validate_contracts >> deploy_notice
