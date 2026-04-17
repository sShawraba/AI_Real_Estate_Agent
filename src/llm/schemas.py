from pydantic import BaseModel
from typing import Optional, List

class ExtractedFeatures(BaseModel):
    Overall_Qual: Optional[int]
    Gr_Liv_Area: Optional[int]
    Full_Bath: Optional[int]
    Garage_Cars: Optional[int]
    Year_Built: Optional[int]
    Neighborhood: Optional[str]
    Bedroom_AbvGr: Optional[int]
    Kitchen_Qual: Optional[str]
    Total_Bsmt_SF: Optional[int]

    missing_fields: List[str]
    confidence: float