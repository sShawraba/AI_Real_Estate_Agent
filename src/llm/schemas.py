from pydantic import BaseModel
from typing import Optional, List

class ExtractedFeatures(BaseModel):
    Overall Qual: Optional[int]
    Gr Liv Area: Optional[int]
    Full Bath: Optional[int]
    Garage Cars: Optional[int]
    Year Built: Optional[int]
    Neighborhood: Optional[str]
    Bedroom AbvGr: Optional[int]
    Kitchen Qual: Optional[str]
    Total Bsmt SF: Optional[int]

    missing_fields: List[str]
    confidence: float