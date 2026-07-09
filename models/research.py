from pydantic import BaseModel, Field
from typing import List, Optional

from models.evidence import Evidence
from models.company import CompanyProfile


class ResearchState(BaseModel):

    company_name: str

    company: Optional[CompanyProfile] = None

    evidence: List[Evidence] = Field(
        default_factory=list
    )