from pydantic import BaseModel
from typing import Optional


class CompanySearchResult(BaseModel):
    company_name: str
    company_number: str
    company_status: Optional[str] = None
    company_type: Optional[str] = None