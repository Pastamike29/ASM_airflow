# repo/schemas/finding.py

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class Finding(BaseModel):
    finding_id: str
    asset: str
    asset_id: str

    port: Optional[int] = None
    protocol: Optional[str] = None
    service: Optional[str] = None

    scanner: str
    asset_type: str
    state: str

    severity: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None

    first_seen: datetime
    last_seen: datetime
