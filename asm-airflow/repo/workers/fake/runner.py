from datetime import UTC, datetime
from typing import List

from repo.schemas.worker_result import WorkerResult
from repo.schemas.finding import Finding
from repo.schemas.scan_job import ScanJob


def run_fake_worker(job: ScanJob) -> WorkerResult:
    findings: List[Finding] = []

    for target in job.targets:
        findings.append(
            Finding(
                finding_id=f"fake:{job.scanner}:{target}",
                asset=target,
                asset_id=f"asset:{target}",
                asset_type="network",
                scanner=job.scanner,
                state="open",

                port=None,
                protocol=None,
                service=None,

                first_seen=datetime.now(UTC),
                last_seen=datetime.now(UTC),
            )
        )

    return WorkerResult(
        job_id=job.job_id,
        stage=job.stage,
        scanner=job.scanner,

        target=",".join(job.targets),
        findings=findings,

        stats={
            "targets": len(job.targets),
            "findings": len(findings),
        },

        finished_at=datetime.now(UTC).isoformat(),
    )