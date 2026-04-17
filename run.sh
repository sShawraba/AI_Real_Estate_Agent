#!/bin/bash
# Run the Streamlit Real Estate Price Prediction App

echo "🚀 Starting Real Estate Price Prediction Engine..."
echo ""
echo "📍 The app will open in your browser at: http://localhost:8501"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

.venv/bin/python -m streamlit run app/streamlit_app.py --logger.level=error
