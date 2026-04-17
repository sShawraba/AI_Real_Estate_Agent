import os
import json

USE_GEMINI = True

def run_gemini(prompt):
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text

def run_openai(prompt):
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def explain_prediction(features: dict, price: float):
    prompt = f"""
You are a real estate expert.

You are given:
- House features: {json.dumps(features)}
- Predicted price: {price}

Task:
Explain in simple terms:
1. Why the price is high or low
2. Which features increased price
3. Which features reduced price
4. Compare it to typical market expectations

Keep it short (5-8 lines max).
No fluff.
"""

    if USE_GEMINI:
        return run_gemini(prompt)
    else:
        return run_openai(prompt)
    

