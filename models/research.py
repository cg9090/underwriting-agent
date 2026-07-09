from pydantic import BaseModel
from typing import List

from models.evidence import Evidence


class ResearchState(BaseModel):

    company_name: str
    evidence: List[Evidence] = []