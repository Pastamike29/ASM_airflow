from repo.schemas.scan_job import ScanJob
from repo.workers.fake.runner import run_fake_worker
from repo.ingest.schema_validation import validate_worker_result


def test_fake_worker_emits_valid_schema():
    job = ScanJob(
        job_id="job-1",
        tenant_id="tenant",
        stage="probe",
        scanner="fake",
        targets=["1.1.1.1"],
    )
    

    result = run_fake_worker(job).model_dump(mode="json", exclude_none=True)
    validate_worker_result(result)
