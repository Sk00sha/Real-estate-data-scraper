from airflow import DAG
from airflow.operators.python import PythonOperator,BranchPythonOperator
from datetime import datetime

with DAG("first_dag"
,start_date=datetime(2022,11,26)
,schedule_interval="@daily"
,catchup=False) as dag:
    step_A=PythonOperator(
        task_id="Task_A",
        python_callable=
        )