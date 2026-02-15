from datetime import datetime, UTC

SAMPLE_WORKER_RESULT = {
    "job_id": "job-123",
    "stage": "probe",
    "scanner": "fake",
    "target": "1.1.1.1",
    "finished_at": datetime.now(UTC).isoformat(),
    "stats": {
        "targets": 1,
        "findings": 1,
    },
    "findings": [
        {
            "finding_id": "fake:1.1.1.1",
            "asset": "1.1.1.1",
            "asset_id": "asset:1.1.1.1",
            "asset_type": "network",
            "scanner": "fake",
            "state": "open",
            "port": None,
            "protocol": None,
            "service": None,
            "first_seen": datetime.now(UTC).isoformat(),
            "last_seen": datetime.now(UTC).isoformat(),
        }
    ],
}
