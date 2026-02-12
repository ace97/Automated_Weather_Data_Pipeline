import sys
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


# Ensure this path is correct on the Airflow worker/scheduler
sys.path.append('/opt/airflow/api-request')

def safe_main_callable():
    from insert_records import main
    return main()


default_args = {
    'owner': 'airflow',
    'description': 'A DAG to orchestrate data',
    'start_date': datetime(2026, 1, 27),
}

dag = DAG(
    'weather-api-dbt-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=5), 
    catchup=False
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data_task',
        python_callable=safe_main_callable
    )

    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(source='/home/anirudh/repos/weather-data-project/dbt/my_project',
                target='/usr/app',
                type='bind'),
            Mount(source='/home/anirudh/repos/weather-data-project/dbt/profiles.yml',
                target='/root/.dbt/profiles.yml',
                type='bind')
        ],
        network_mode='weather-data-project_my-network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success'
    )

task1 >> task2