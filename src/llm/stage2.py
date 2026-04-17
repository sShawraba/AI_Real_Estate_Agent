import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

USE_GEMINI = True

def run_gemini(prompt):
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Please add it to your .env file. "
            "Get it from: https://aistudio.google.com/app/apikeys"
        )

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-3-flash-preview")
    response = model.generate_content(prompt)

    return response.text

def run_openai(prompt):
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. Please add it to your .env file. "
            "Get it from: https://platform.openai.com/api-keys"
        )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def explain_prediction(features: dict, price: float, market_stats: dict = None):
    """
    Interpret the ML prediction with context.
    
    Args:
        features: Dict of extracted house features
        price: Predicted price from ML model
        market_stats: Dict with 'median_price' and 'price_range' (tuple)
    """
    
    # Default market stats if not provided
    if market_stats is None:
        market_stats = {
            "median_price": 180000,
            "price_range": (50000, 500000)
        }
    
    median_price = market_stats.get("median_price", 180000)
    price_range = market_stats.get("price_range", (50000, 500000))
    
    # Determine if price is high/low/typical
    if price > price_range[1]:
        range_assessment = f"exceptionally high (above ${price_range[1]:,.0f})"
    elif price > median_price * 1.3:
        range_assessment = f"well above market median (${median_price:,.0f})"
    elif price < price_range[0]:
        range_assessment = f"exceptionally low (below ${price_range[0]:,.0f})"
    elif price < median_price * 0.7:
        range_assessment = f"below market median"
    else:
        range_assessment = "typical market value"
    
    prompt = f"""
You are a real estate expert providing a brief price interpretation.

**House Features:**
{json.dumps(features, indent=2)}

**Predicted Price:** ${price:,.0f}

**Market Context:**
- Median price in market: ${median_price:,.0f}
- Typical range: ${price_range[0]:,.0f} - ${price_range[1]:,.0f}
- This prediction is: {range_assessment}

**Your Task:**
Provide a brief, professional interpretation (4-6 sentences):
1. Is the price high, low, or typical for the market?
2. Which 2-3 features most significantly drive the price (up or down)?
3. One key observation about market positioning

Format: Natural language, conversational tone. No bullet points.
"""

    if USE_GEMINI:
        return run_gemini(prompt)
    else:
        return run_openai(prompt)
    

