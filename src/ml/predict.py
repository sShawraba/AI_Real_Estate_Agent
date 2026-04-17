import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join("models", "xgb_model.pkl")

model = joblib.load(MODEL_PATH)

FEATURE_MAP = {
    "Overall_Qual": "Overall Qual",
    "Gr_Liv_Area": "Gr Liv Area",
    "Full_Bath": "Full Bath",
    "Garage_Cars": "Garage Cars",
    "Year_Built": "Year Built",
    "Neighborhood": "Neighborhood",
    "Bedroom_Abvgr": "Bedroom AbvGr",
    "Kitchen_Qual": "Kitchen Qual",
    "Total_Bsmt_Sf": "Total Bsmt SF"
}

# from llm output to model input
def prepare_input(features: dict):
    converted = {}

    for llm_key, model_key in FEATURE_MAP.items():
        value = features.get(llm_key)

        # IMPORTANT: keep None, let sklearn pipeline handle it
        converted[model_key] = value

    # return single-row dataframe
    return pd.DataFrame([converted])

def predict_price(features: dict):
    df = prepare_input(features)

    prediction = model.predict(df)[0]

    return float(prediction)

def get_model_info():
    return {
        "model_type": "XGBoost Pipeline",
        "features": list(FEATURE_MAP.values())
    }