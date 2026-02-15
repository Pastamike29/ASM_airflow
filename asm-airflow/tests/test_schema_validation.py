import pytest
from repo.ingest.schema_validation import validate_worker_result


def test_valid_worker_result_passes(sample_worker_result):
    validate_worker_result(sample_worker_result)


def test_missing_required_field_fails(sample_worker_result):
    del sample_worker_result["job_id"]

    with pytest.raises(ValueError):
        validate_worker_result(sample_worker_result)


def test_extra_field_fails(sample_worker_result):
    sample_worker_result["unexpected"] = "boom"

    with pytest.raises(ValueError):
        validate_worker_result(sample_worker_result)
