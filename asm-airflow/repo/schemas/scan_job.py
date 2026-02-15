from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ScanPolicy(BaseModel):
    rate_limit: Optional[int] = None
    scan_window: Optional[str] = None
    exclusions: List[str] = []


class ScanJob(BaseModel):
    job_id: str
    tenant_id: str

    stage: Literal["discovery", "probe", "vuln", "enrich"]
    scanner: str

    targets: List[str]

    policy: ScanPolicy = Field(default_factory=ScanPolicy)

    parent_job_id: Optional[str] = None
