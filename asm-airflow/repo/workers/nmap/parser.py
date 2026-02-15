from datetime import datetime
import hashlib

from datetime import UTC
import xmltodict
from repo.schemas.finding import Finding
from repo.schemas.worker_result import WorkerResult


def stable_id(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def parse_nmap_result(result: WorkerResult) -> list[Finding]:
    findings: list[Finding] = []

    for host in result.raw.get("hosts", []):
        addr = host["address"]
        for port in host.get("ports", []):
            if port["state"] != "open":
                continue

            findings.append(
                Finding(
                    finding_id=f"nmap:{addr}:{port['port']}",
                    asset=addr,
                    asset_id=f"asset:{addr}",
                    asset_type="network",
                    scanner="nmap",
                    state="open",
                    port=port["port"],
                    protocol=port["proto"],
                    service=port.get("service"),
                    first_seen=datetime.now(UTC),
                    last_seen=datetime.now(UTC),
                )
            )

    return findings


def nmap_xml_to_raw(xml: str) -> dict:
    parsed = xmltodict.parse(xml)

    hosts = parsed["nmaprun"].get("host", [])
    if isinstance(hosts, dict):
        hosts = [hosts]

    normalized = []

    for host in hosts:
        addr = host["address"]["@addr"]
        ports = host.get("ports", {}).get("port", [])

        if isinstance(ports, dict):
            ports = [ports]

        normalized_ports = []
        for p in ports:
            normalized_ports.append({
                "port": int(p["@portid"]),
                "proto": p["@protocol"],
                "state": p["state"]["@state"],
                "service": p.get("service", {}).get("@name"),
            })

        normalized.append({
            "address": addr,
            "ports": normalized_ports,
            "meta": {},
        })
    

    return {"hosts": normalized}
