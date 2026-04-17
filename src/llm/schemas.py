from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ExtractedFeatures(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    overall_qual: Optional[int] = None
    gr_liv_area: Optional[int] = None
    full_bath: Optional[int] = None
    garage_cars: Optional[int] = None
    year_built: Optional[int] = None
    neighborhood: Optional[str] = None
    bedroom_abvgr: Optional[int] = None
    kitchen_qual: Optional[str] = None
    total_bsmt_sf: Optional[int] = None
    
    missing_fields: List[str] = []
    confidence: float = 0.0