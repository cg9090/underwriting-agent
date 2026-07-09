from pydantic import BaseModel
from typing import Optional


class Evidence(BaseModel):
    claim: str
    source: str
    url: Optional[str] = None
    category: str
    confidence: float