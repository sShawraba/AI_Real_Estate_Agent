from src.llm.stage1 import extract_features
from src.ml.predict import predict_price
from src.llm.stage2 import explain_prediction

def run_pipeline(user_input: str):
    # 1. Stage 1 → extract structured features
    extracted = extract_features(user_input)

    # handle LLM failure
    if isinstance(extracted, dict) and "error" in extracted:
        return {
            "status": "error",
            "step": "stage1",
            "details": extracted
        }

    features_dict = extracted.dict() #features_dict = extracted.model_dump() if pydantic v2

    # 2. check missing fields
    missing = features_dict.get("missing_fields", [])

    if missing:
        return {
            "status": "needs_input",
            "missing_fields": missing,
            "extracted_features": features_dict
        }

    # 3. ML prediction
    price = predict_price(features_dict)

    # 4. Stage 2 explanation (we will implement next)
    explanation = explain_prediction(features_dict, price)

    return {
        "status": "success",
        "features": features_dict,
        "predicted_price": price,
        "explanation": explanation
    }

