import streamlit as st
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.llm.stage1 import extract_features
from src.ml.predict import predict_price, FEATURE_MAP
from src.llm.stage2 import explain_prediction


def check_api_keys():
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    return bool(gemini_key or openai_key)


st.set_page_config(page_title="Real Estate Predictor", page_icon="🏠", layout="centered")
st.title("🏠 Real Estate Price Predictor")

if not check_api_keys():
    st.error("⚠️ API keys not configured. See API_KEY_SETUP.md")
    st.stop()

# Input
user_input = st.text_area(
    "Describe the property:",
    placeholder="3 bed, 2 bath, 2500 sqft, built 2005, downtown, good condition...",
    height=80
)

if st.button("🔍 Analyze", type="primary", use_container_width=True):
    if not user_input.strip():
        st.error("Please enter a description")
        st.stop()

    col1, col2 = st.columns(2)
    
    # Stage 1: Extract
    with col1:
        with st.spinner("Extracting features..."):
            try:
                extracted = extract_features(user_input)
                if isinstance(extracted, dict) and "error" in extracted:
                    st.error(f"❌ {extracted.get('message')}")
                    st.stop()
                features_dict = extracted.model_dump()
                st.success("✅ Features extracted")
            except Exception as e:
                st.error(f"❌ {str(e)}")
                st.stop()
    
    # Stage 2: Predict
    with col2:
        with st.spinner("Predicting price..."):
            try:
                pred_features = {key: features_dict.get(key) for key in FEATURE_MAP.keys()}
                predicted_price = predict_price(pred_features)
                st.success("✅ Price predicted")
            except Exception as e:
                st.error(f"❌ {str(e)}")
                st.stop()
    
    st.divider()
    
    # Results
    st.markdown(f"## Predicted Price: **${predicted_price:,.0f}**")
    
    # Extracted Features (3 columns)
    st.markdown("### Extracted Features")
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    features_list = [
        ("overall_qual", "Quality"),
        ("gr_liv_area", "Living Area (sqft)"),
        ("full_bath", "Bathrooms"),
        ("garage_cars", "Garage Capacity"),
        ("year_built", "Year Built"),
        ("total_bsmt_sf", "Basement (sqft)"),
        ("bedroom_abvgr", "Bedrooms"),
        ("neighborhood", "Neighborhood"),
        ("kitchen_qual", "Kitchen Quality"),
    ]
    
    feat_cols = [feat_col1, feat_col2, feat_col3]
    for idx, (key, label) in enumerate(features_list):
        with feat_cols[idx % 3]:
            val = features_dict.get(key)
            st.metric(label, val if val is not None else "—")
    
    # Market comparison
    st.markdown("### Market Context")
    market_median = 180000
    diff = predicted_price - market_median
    pct = (diff / market_median) * 100
    
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.metric("Market Median", f"${market_median:,.0f}")
    with mc2:
        st.metric("vs. Median", f"{pct:+.1f}%", f"${diff:+,.0f}")
    with mc3:
        st.metric("Confidence", f"{features_dict.get('confidence', 0):.0%}")
    
    # Stage 3: Interpretation
    st.markdown("### Expert Analysis")
    with st.spinner("Analyzing..."):
        try:
            market_stats = {"median_price": market_median, "price_range": (50000, 500000)}
            interpretation = explain_prediction(features_dict, predicted_price, market_stats)
            st.info(interpretation)
        except Exception as e:
            st.warning(f"Analysis unavailable: {str(e)}")
    
    # Export
    st.divider()
    summary = {
        "timestamp": datetime.now().isoformat(),
        "input": user_input,
        "features": features_dict,
        "predicted_price": predicted_price,
    }
    
    st.json(summary, expanded=False)

