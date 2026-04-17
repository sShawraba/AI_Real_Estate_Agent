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
- FastAPI backend
- Dockerized deployment

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🚀 Run with docker
```bash
docker build -t real-estate-ai .
docker run -p 8000:8000 real-estate-ai