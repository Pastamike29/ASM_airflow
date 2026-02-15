import copy
from datetime import datetime, timezone
import pytest
from pathlib import Path
from .fixtures.sample_worker_result import SAMPLE_WORKER_RESULT



@pytest.fixture
def sample_nmap_xml():
    return (Path(__file__).parent / "fixtures" / "nmap_simple.xml").read_text()

@pytest.fixture
def sample_worker_result():
    now = datetime.now(timezone.utc).isoformat()

    return {
        "job_id": "job-123",
        "stage": "probe",
        "scanner": "fake",
        "target": "1.1.1.1",
        "finished_at": now,
        "stats": {
            "targets": 1,
            "findings": 1,
        },
        "errors": [],
        "findings": [
            {
                "finding_id": "fake:fake:1.1.1.1",
                "asset": "1.1.1.1",
                "asset_id": "asset:1.1.1.1",
                "asset_type": "network",
                "scanner": "fake",
                "state": "open",
                "port": 80,
                "protocol": "tcp",
                "service": "http",
                "first_seen": now,
                "last_seen": now,
            }
        ],
    }