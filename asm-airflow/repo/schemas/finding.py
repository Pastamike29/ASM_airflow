# repo/schemas/finding.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Finding:
    finding_id: str
    asset: str
    asset_id: str
    port: Optional[int]
    protocol: Optional[str]
    service: Optional[str]

    scanner: str
    asset_type: str
    state: str

    severity: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None

    first_seen: datetime = None
    last_seen: datetime = None
