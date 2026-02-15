import json
from repo.workers.nmap.runner import run_nmap_worker
from repo.schemas.scan_job import ScanJob
from tests.utils.schema_assertions import assert_shape


def test_nmap_worker_schema_contract(sample_nmap_xml):
    job = ScanJob(
        job_id="job-2",
        tenant_id="tenant",
        stage="probe",
        scanner="nmap",
        targets=["1.1.1.1"],
    )

    result = run_nmap_worker(job, xml_override=sample_nmap_xml).model_dump()

    with open("tests/golden/worker_result_contract.json") as f:
        contract = json.load(f)

    assert_shape(result, contract)
