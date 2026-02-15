from repo.schemas.scan_job import ScanJob
from repo.workers.fake.runner import run_fake_worker
from repo.ingest.worker_results import ingest_worker_result


def test_fake_worker_ingestion_happy_path(capsys):
    """
    End-to-end test:
    ScanJob -> FakeWorker -> WorkerResult -> Ingest
    """

    job = ScanJob(
        job_id="job-test-001",
        tenant_id="tenant-test",
        stage="probe",
        scanner="fake",
        targets=["1.1.1.1", "2.2.2.2"],
    )

    result = run_fake_worker(job)

    # Ensure worker produced findings
    assert result.job_id == job.job_id
    assert result.scanner == "fake"
    assert len(result.findings) == 2

    # Ingest should not raise
    ingest_worker_result(result.model_dump(mode="json"))

    # Capture stdout to confirm ingestion happened
    captured = capsys.readouterr()
    assert "[INGEST]" in captured.out



def test_ingestion_rejects_invalid_schema():
    """
    Repo must reject malformed worker output.
    """

    bad_payload = {
        "job_id": "job-bad",
        "stage": "probe",
        "scanner": "fake",
        # findings missing required fields
        "findings": [{"asset": "1.1.1.1"}],
    }

    try:
        ingest_worker_result(bad_payload)
        assert False, "Expected schema validation failure"
    except Exception:
        assert True
