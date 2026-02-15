# dags/asm_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from repo.ingest.worker_results import ingest_worker_results
from repo.schemas.worker_result import WorkerResult


def discovery_task(**context):
    # placeholder
    return ["example.com", "test.example.com"]


def run_nmap_task(**context):
    # mocked worker output (70% stage)
    return WorkerResult(
        job_id="job-1",
        scanner="nmap",
        target="example.com",
        raw={
            "hosts": [
                {
                    "address": "example.com",
                    "ports": [
                        {"port": 80, "proto": "tcp", "service": {"name": "http"}},
                        {"port": 443, "proto": "tcp", "service": {"name": "https"}},
                    ],
                }
            ]
        },
        finished_at=datetime.utcnow().isoformat(),
    )


def ingest_task(**context):
    ti = context["ti"]
    worker_result = ti.xcom_pull(task_ids="nmap")

    findings = ingest_worker_results([worker_result])

    print(f"[+] Normalized findings: {len(findings)}")
    return [f.finding_id for f in findings]


with DAG(
    dag_id="asm_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    discovery = PythonOperator(
        task_id="discovery",
        python_callable=discovery_task,
    )

    nmap = PythonOperator(
        task_id="nmap",
        python_callable=run_nmap_task,
    )

    ingest = PythonOperator(
        task_id="ingest",
        python_callable=ingest_task,
        provide_context=True,
    )

    discovery >> nmap >> ingest
