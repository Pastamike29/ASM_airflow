from pathlib import Path
from repo.workers.nmap.parser import nmap_xml_to_raw


FIXTURES = Path(__file__).parent.parent.parent / "fixtures"


def test_parse_nmap_xml_single_host():
    xml = (FIXTURES / "nmap_simple.xml").read_text()

    result = nmap_xml_to_raw(xml)

    assert "hosts" in result
    assert len(result["hosts"]) == 1

    host = result["hosts"][0]
    assert host["address"] == "1.1.1.1"

    ports = host["ports"]
    assert len(ports) == 2

    assert ports[0] == {
        "port": 80,
        "proto": "tcp",
        "state": "open",
        "service": "http",
    }

    assert ports[1]["port"] == 22
    assert ports[1]["state"] == "closed"
    
def test_parse_nmap_xml_no_ports():
    xml = """<?xml version="1.0"?>
    <nmaprun>
      <host>
        <address addr="2.2.2.2" addrtype="ipv4"/>
      </host>
    </nmaprun>
    """

    result = nmap_xml_to_raw(xml)
    assert result["hosts"][0]["ports"] == []


def test_parse_nmap_xml_multiple_hosts():
    xml = """<?xml version="1.0"?>
    <nmaprun>
      <host>
        <address addr="1.1.1.1" addrtype="ipv4"/>
      </host>
      <host>
        <address addr="2.2.2.2" addrtype="ipv4"/>
      </host>
    </nmaprun>
    """

    result = nmap_xml_to_raw(xml)
    assert len(result["hosts"]) == 2

