from pydantic import BaseModel
from typing import Optional, List


class CompanyProfile(BaseModel):
    company_name: str
    company_number: str
    status: Optional[str] = None
    incorporation_date: Optional[str] = None
    sic_codes: List[str] = []
    registered_address: Optional[str] = None