import pytest
from repo.ingest.worker_results import ingest_worker_result


def test_ingest_accepts_valid_result(sample_worker_result):
    ingest_worker_result(sample_worker_result)


def test_ingest_rejects_invalid_result(sample_worker_result):
    sample_worker_result.pop("finished_at")

    with pytest.raises(ValueError):
        ingest_worker_result(sample_worker_result)
     