# AI Real Estate Agent

This project is an AI-powered real estate price prediction system using LLM prompt chaining + machine learning.

---

## 🧠 Architecture

User input → LLM (feature extraction) → ML model (XGBoost pipeline) → LLM (explanation)

---

## 📦 Features

- Natural language house description input
- LLM extracts structured features (Stage 1)
- XGBoost pipeline predicts house price
- LLM explains prediction (Stage 2)
- Handles missing features interactively
- Streamlit web interface
- FastAPI backend
- Dockerized deployment

---

## 🔑 Setup: Configure API Keys

> ⚠️ **Required**: You must set up API keys before running the app.

### Step 1: Create `.env` file

```bash
cp .env.example .env
```

### Step 2: Add your API keys to `.env`

Edit `.env` and add your keys:

```env
# Get from: https://aistudio.google.com/app/apikeys
GEMINI_API_KEY=your_gemini_key_here

# Optional: Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_key_here
```

### Step 3: Verify keys are loaded

```bash
python check_api_keys.py
```

You should see:
```
✓ GEMINI_API_KEY:  abc123***xyz
✓ Gemini API working: Hello!
```

---

## 🚀 Quick Start (Streamlit UI)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Make sure .env file is configured (see above)

# 3. Run the app
bash run.sh
```

The app opens at: **http://localhost:8501**

---

## 📊 Using the Streamlit App

1. **Enter property description** (natural language)
   - Example: "3 bed, 2 bath, 2500 sqft, built 2005, downtown location"

2. **Click "Analyze Property"**
   - Stage 1: LLM extracts features
   - Stage 2: ML model predicts price
   - Stage 3: LLM explains the prediction

3. **Review results**
   - Extracted features with confidence scores
   - Predicted price with market comparison
   - Expert interpretation & analysis

See [APP_GUIDE.md](APP_GUIDE.md) for complete documentation.

---

## 🚀 Run FastAPI Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

API runs at: **http://localhost:8000**

Docs: **http://localhost:8000/docs**

---

## 🐳 Docker Deployment (Production)

### Build & Run with Docker

```bash
# 1. Ensure .env file exists with API keys
cp .env.example .env  # Fill in your API keys

# 2. Build image (includes trained model)
docker build -t real-estate-api .

# 3. Run container
docker run -p 8000:8000 --env-file .env real-estate-api

# 4. Test the API
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"property_description":"3 bed, 2 bath, 2500 sqft, built 2005"}'
```

### Or with Docker Compose (Recommended)

```bash
docker-compose up --build
```

### API Endpoints

- **POST /predict** - Main prediction endpoint  
  Query: Property description  
  Returns: Validated JSON with predictions

- **GET /health** - Health check  

- **GET /docs** - Swagger documentation (http://localhost:8000/docs)

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for complete deployment guide.

---