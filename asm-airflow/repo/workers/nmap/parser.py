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


def nmap_xml_to_raw(xml_output: str) -> list[dict]:
    import xml.etree.ElementTree as ET

    root = ET.fromstring(xml_output)

    hosts = []

    for host in root.findall("host"):
        
        address_elem = host.find("address")
        if address_elem is None:
            continue

        address = address_elem.get("addr")

        ports = []
        ports_elem = host.find("ports")
        if ports_elem is not None:
            for port_elem in ports_elem.findall("port"):
                state_elem = port_elem.find("state")
                service_elem = port_elem.find("service")

                ports.append({
                    "port": int(port_elem.get("portid")),
                    "proto": port_elem.get("protocol"),
                    "state": state_elem.get("state") if state_elem is not None else None,
                    "service": service_elem.get("name") if service_elem is not None else None,
                })

        hosts.append({
            "address": address,
            "ports": ports,
        })


    return {"hosts": hosts}

