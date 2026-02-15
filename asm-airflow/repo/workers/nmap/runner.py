import subprocess
from datetime import datetime, UTC, timezone
from typing import Dict, Any

from repo.schemas.scan_job import ScanJob
from repo.schemas.worker_result import WorkerResult
from .parser import nmap_xml_to_raw
from repo.schemas.finding import Finding


def compute_stats(raw: Dict[str, Any]) -> Dict[str, int]:
    hosts = raw.get("hosts", [])

    hosts_up = sum(1 for h in hosts if h.get("status") == "up")
    ports_open = sum(
        1
        for h in hosts
        for p in h.get("ports", [])
        if p.get("state") == "open"
    )

    return {
        "hosts_up": hosts_up,
        "ports_open": ports_open,
    }


def run_nmap_worker(job: ScanJob, xml_override: str | None = None):
     
    if xml_override is not None:
        xml_output = xml_override
    else:
        proc = subprocess.run(
            ["nmap", "-p", "1-1000", "-oX", "-", job.targets[0]],
            capture_output=True,
            text=True,
            check=True,
        )
        xml_output = proc.stdout

    # Step 1: parse raw XML
    raw_hosts = nmap_xml_to_raw(xml_output)

    findings = []

    for host in raw_hosts:
        address = host["address"]

        for port in host.get("ports", []):
            if port.get("state") != "open":
                continue

            findings.append(
                Finding(
                    finding_id=f"nmap:{address}:{port['port']}",
                    asset=address,
                    asset_id=f"asset:{address}",
                    asset_type="network",
                    scanner="nmap",
                    state="open",
                    port=port["port"],
                    protocol=port.get("protocol"),
                    service=port.get("service"),
                    first_seen=datetime.now(UTC),
                    last_seen=datetime.now(UTC),
                )
            )

    return WorkerResult(
        job_id=job.job_id,
        stage=job.stage,
        scanner=job.scanner,
        target=job.targets[0],
        finished_at=datetime.now(UTC),
        findings=findings,
        errors=[],
        stats={
            "hosts_up": len(raw_hosts),
            "ports_open": len(findings),
        },
    )
