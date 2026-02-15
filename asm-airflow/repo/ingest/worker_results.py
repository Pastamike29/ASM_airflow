# ingest/worker_results.py
from typing import Any, Dict, List

from repo.schemas.worker_result import WorkerResult
from repo.schemas.finding import Finding
from repo.ingest.schema_validation import validate_worker_result
from repo.workers.nmap.parser import parse_nmap_result

def ingest(payload: dict):
    validate_worker_result(payload)   # ← ADD THIS LINE

    print(f"[INGEST] job_id={payload['job_id']} findings={len(payload['findings'])}")

def ingest_worker_result(worker_result: Dict[str, Any]) -> List[Finding]:
    validate_worker_result(worker_result)   # ← ADD THIS

    findings = worker_result.get("findings", [])

    print(f"[INGEST] job_id={worker_result.get('job_id')} findings={len(findings)}")

    return findings


