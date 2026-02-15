import json
from pathlib import Path

from repo.schemas.scan_job import ScanJob
from repo.workers.fake.runner import run_fake_worker
from tests.utils.schema_assertions import assert_shape


def test_fake_worker_schema_contract():
    job = ScanJob(
        job_id="job-1",
        tenant_id="tenant",
        stage="probe",
        scanner="fake",
        targets=["1.1.1.1"],
    )

    result = run_fake_worker(job).model_dump(mode="json")

    contract_path = (
        Path(__file__).parent / "golden" / "worker_result_contract.json"
    )


    with contract_path.open() as f:
        contract = json.load(f)

    assert_shape(result, contract)
    
