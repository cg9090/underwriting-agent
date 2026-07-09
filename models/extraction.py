from pydantic import BaseModel
from typing import List, Optional


class ExtractionResult(BaseModel):

    claims: List[dict] = []

    error: Optional[str] = None