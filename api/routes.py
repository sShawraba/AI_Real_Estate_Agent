from fastapi import APIRouter
from pydantic import BaseModel
from src.pipeline import run_pipeline

router = APIRouter()
class QueryRequest(BaseModel):
    user_input: str

@router.post("/predict")
def predict(request: QueryRequest):
    result = run_pipeline(request.user_input)
    return result