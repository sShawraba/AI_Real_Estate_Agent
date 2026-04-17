from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.llm.stage1 import extract_features
from src.ml.predict import predict_price, FEATURE_MAP
from src.llm.stage2 import explain_prediction
from src.llm.schemas import ExtractedFeatures

router = APIRouter()


# ============== REQUEST MODELS ==============
class PredictionRequest(BaseModel):
    """Input: Property description"""
    property_description: str = Field(..., min_length=10, description="Natural language property description")
    market_median: Optional[float] = Field(default=180000, description="Market median price for context")


# ============== RESPONSE MODELS ==============
class PredictionResponse(BaseModel):
    """Complete prediction response with all extracted info"""
    timestamp: str
    input: str
    extracted_features: Dict[str, Any]
    predicted_price: float
    market_context: Dict[str, Any]
    interpretation: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2026-04-17T10:30:00",
                "input": "3 bed, 2 bath, 2500 sqft, built 2005...",
                "extracted_features": {
                    "overall_qual": 7,
                    "gr_liv_area": 2500,
                    "full_bath": 2,
                    "garage_cars": 2,
                    "year_built": 2005,
                    "neighborhood": "Downtown",
                    "bedroom_abvgr": 3,
                    "kitchen_qual": "Gd",
                    "total_bsmt_sf": 1200,
                    "confidence": 0.92,
                    "missing_fields": []
                },
                "predicted_price": 245000.00,
                "market_context": {
                    "median_price": 180000,
                    "price_difference": 65000,
                    "price_percentage": 36.1
                },
                "interpretation": "This property is priced above market..."
            }
        }


# ============== ENDPOINTS ==============
@router.post("/predict", response_model=PredictionResponse, summary="Predict house price from description")
async def predict(request: PredictionRequest):
    """
    Complete 3-stage pipeline: Extract → Predict → Interpret
    
    Takes a property description and returns:
    - Extracted features (9 key attributes)
    - Predicted price using XGBoost model
    - Expert interpretation with market context
    
    **Query:** Property description (natural language)
    
    **Response:** Validated JSON with all extracted information
    """
    
    try:
        # ============= STAGE 1: Extract =============
        extracted = extract_features(request.property_description)
        
        if isinstance(extracted, dict) and "error" in extracted:
            raise HTTPException(
                status_code=422,
                detail=f"Feature extraction failed: {extracted.get('message')}"
            )
        
        features_dict = extracted.model_dump()
        
        # ============= STAGE 2: Predict =============
        pred_features = {key: features_dict.get(key) for key in FEATURE_MAP.keys()}
        predicted_price = predict_price(pred_features)
        
        # ============= STAGE 3: Interpret =============
        market_stats = {
            "median_price": request.market_median,
            "price_range": (50000, 500000)
        }
        interpretation = explain_prediction(features_dict, predicted_price, market_stats)
        
        # ============= BUILD RESPONSE =============
        price_diff = predicted_price - request.market_median
        price_pct = (price_diff / request.market_median) * 100
        
        response = PredictionResponse(
            timestamp=datetime.now().isoformat(),
            input=request.property_description,
            extracted_features=features_dict,
            predicted_price=predicted_price,
            market_context={
                "median_price": request.market_median,
                "price_difference": price_diff,
                "price_percentage": round(price_pct, 1)
            },
            interpretation=interpretation
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction pipeline error: {str(e)}"
        )


@router.get("/health", summary="Health check")
async def health_check():
    """System health status"""
    return {
        "status": "healthy",
        "service": "Real Estate Price Predictor",
        "version": "1.0"
    }