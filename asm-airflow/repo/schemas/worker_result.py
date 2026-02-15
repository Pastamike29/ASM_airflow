from typing import List, Dict, Literal
from pydantic import BaseModel, Field

from repo.schemas.finding import Finding


class WorkerResult(BaseModel):
    job_id: str
    stage: Literal["discovery", "probe", "vuln", "enrich"]
    scanner: str
    target: str

    findings: List[Finding] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

    stats: Dict[str, int] = Field(default_factory=dict)
    finished_at: str
