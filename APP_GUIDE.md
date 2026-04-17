# 🏠 Real Estate Price Prediction Engine - Streamlit Interface

## Overview

The Streamlit interface connects the complete 3-stage AI pipeline for real estate valuation:

```
User Input → Stage 1 (LLM) → Stage 2 (ML) → Stage 3 (LLM) → Expert Prediction
```

## Architecture

### Stage 1: Feature Extraction 🔍
- **Input**: Natural language property description
- **Process**: Google Gemini/GPT-4 LLM extracts structured features
- **Output**: Validated `ExtractedFeatures` Pydantic model
- **Features Extracted**:
  - Overall Quality (1-10)
  - Living Area (sqft)
  - Number of Bathrooms
  - Garage Capacity
  - Year Built
  - Neighborhood
  - Bedrooms Above Grade
  - Kitchen Quality (Po/Fa/TA/Gd/Ex)
  - Basement Square Footage
  - Confidence score & Missing fields

### Stage 2: ML Prediction 🤖
- **Input**: Structured features from Stage 1
- **Model**: XGBoost pipeline with 9-feature training
- **Output**: Predicted house price
- **Files**: 
  - `src/ml/predict.py` - Model inference
  - `models/xgb_model.pkl` - Trained model

### Stage 3: Interpretation 📊
- **Input**: Extracted features + predicted price + market stats
- **Process**: GPT/Gemini provides expert analysis
- **Output**: Human-readable interpretation with:
  - Price positioning (high/low/typical)
  - Key drivers of price
  - Market comparison
  - Investment perspective

## Running the App

### Quick Start

```bash
# Clone/navigate to repo
cd /home/soup/ai-real-estate-agent

# Install dependencies (one-time)
python -m pip install -r requirements.txt

# Run the app
bash run.sh
```

The app will start at `http://localhost:8501`

### Manual Start

```bash
.venv/bin/python -m streamlit run app/streamlit_app.py
```

## Usage Guide

### 1. Enter Property Description
```
Example: "3 bedroom, 2 bathroom house in downtown area, 
built in 2005, excellent condition, 2500 sqft living area, 
2 car garage, recently renovated kitchen"
```

### 2. Click "Analyze Property"

The app will:
1. Extract features (Stage 1)
2. Generate prediction (Stage 2)
3. Provide expert analysis (Stage 3)

### 3. Review Results

**Features Panel**: See what features were extracted
- Green cards indicate successfully extracted features
- Yellow warning shows confidence score

**Price Panel**: The ML model's prediction
- Shows predicted price
- Compares to market median
- Displays model type

**Interpretation Panel**: Expert analysis
- Explains why price is positioned there
- Highlights key drivers
- Provides market context

## Configuration

### Environment Variables

```bash
# In .env file
GEMINI_API_KEY=<your-key>  # For Google Gemini
OPENAI_API_KEY=<your-key>   # For OpenAI as fallback
```

### API Selection

Toggle in the sidebar:
- ✅ **Gemini**: Faster, better for extraction
- ❌ **OpenAI**: Fallback option

## File Structure

```
app/
├── streamlit_app.py          # Main UI (this file)
├── requirements.txt          # Dependencies
└── run.sh                    # Startup script

src/
├── llm/
│   ├── stage1.py            # Feature extraction
│   ├── stage2.py            # Interpretation
│   ├── prompts.py           # LLM prompts
│   └── schemas.py           # Pydantic models
├── ml/
│   └── predict.py           # ML model inference
└── pipeline.py              # Complete pipeline

models/
└── xgb_model.pkl            # Trained XGBoost model
```

## Example Flow

```
User: "That lovely 1990s suburban home with 4 bedrooms, 
       2.5 baths, nice big backyard, built around 1992,
       living area about 2200 sq ft"

Stage 1 Output:
{
  "overall_qual": 7,
  "gr_liv_area": 2200,
  "full_bath": 2,
  "garage_cars": 2,
  "year_built": 1992,
  "neighborhood": "Suburban",
  "bedroom_abvgr": 4,
  "kitchen_qual": "Gd",
  "total_bsmt_sf": 1100,
  "confidence": 0.92
}

Stage 2 Output:
Predicted Price: $245,000

Stage 3 Output:
"This 1992 suburban home is priced at $245,000, which 
is solidly above the market median of $180,000 by about 
36%. The larger living area (2200 sq ft) and extra bedroom 
are the primary drivers of the premium pricing. Contemporary 
kitchen and good overall condition further support the 
valuation in a growing suburban market segment."
```

## Features

- ✅ Real-time feature extraction validation
- ✅ Confidence scores for extractions
- ✅ Missing field detection
- ✅ Market context integration
- ✅ Price positioning analysis
- ✅ Results export (JSON)
- ✅ Error handling with fallbacks
- ✅ API toggle (Gemini/OpenAI)

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pydantic'"
```bash
.venv/bin/python -m pip install pydantic
```

### Issue: "Could not connect to Gemini API"
- Check `GEMINI_API_KEY` in `.env`
- Toggle to OpenAI in sidebar as fallback

### Issue: "Model file not found"
- Ensure `models/xgb_model.pkl` exists
- Train model if missing: `python src/pipeline.py`

### Issue: Stage predictions seem off
- Verify feature extraction confidence in output
- Review which fields were missing
- Check if neighborhood is recognized

## Architecture Diagram

```
┌─────────────────────────────────────┐
│  User Input (Natural Language)      │
└──────────────┬──────────────────────┘
               │
         Stage 1: LLM
               │
┌──────────────▼──────────────────────┐
│  Extracted Features (JSON)           │
│  ✓ 9 structured features             │
│  ✓ Confidence score                  │
│  ✓ Missing fields list               │
└──────────────┬──────────────────────┘
               │
         Stage 2: ML
               │
┌──────────────▼──────────────────────┐
│  Predicted Price ($)                 │
│  ✓ XGBoost model                     │
│  ✓ Single prediction value           │
└──────────────┬──────────────────────┘
               │
         Stage 3: LLM
               │
┌──────────────▼──────────────────────┐
│  Expert Interpretation               │
│  ✓ Market positioning                │
│  ✓ Price drivers                     │
│  ✓ Professional analysis             │
└─────────────────────────────────────┘
```

## Advanced Usage

### Export Results Programmatically

```python
from src.llm.stage1 import extract_features
from src.ml.predict import predict_price
from src.llm.stage2 import explain_prediction
import json

# Stage 1
features = extract_features("3 bed, 2 bath, 2500 sqft...")

# Stage 2
price = predict_price(features.model_dump())

# Stage 3
explanation = explain_prediction(
    features.model_dump(), 
    price,
    market_stats={
        "median_price": 180000,
        "price_range": (50000, 500000)
    }
)

# Export
result = {
    "features": features.model_dump(),
    "predicted_price": price,
    "interpretation": explanation
}
print(json.dumps(result, indent=2))
```

## Performance

- **Stage 1**: ~3-5 seconds (LLM + parsing)
- **Stage 2**: ~100ms (ML inference)
- **Stage 3**: ~2-4 seconds (LLM generation)
- **Total**: ~5-10 seconds per analysis

## Limitations & Future Improvements

### Current Limitations
- Requires valid API keys (Gemini/OpenAI)
- Limited to 9 pre-trained features
- No confidence intervals on prediction
- Market stats are hardcoded

### Future Improvements
- [ ] Add prediction confidence intervals
- [ ] Historical price trends
- [ ] Comparable sales analysis
- [ ] Seasonal adjustments
- [ ] Batch processing
- [ ] API endpoint for external apps
- [ ] User accounts & saved analyses
- [ ] Model retraining pipeline

## Support

For issues or questions:
1. Check troubleshooting section above
2. Verify API keys in `.env`
3. Review logs: `streamlit run app/streamlit_app.py --logger.level=debug`
4. Check stage 1/2/3 outputs individually
