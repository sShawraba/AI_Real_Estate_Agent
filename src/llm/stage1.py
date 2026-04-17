import os
import re
import json
from src.llm.schemas import ExtractedFeatures
from src.llm.prompts import STAGE1_PROMPT

USE_GEMINI = True  # switch anytime

# ---------------- GEMINI ----------------
def run_gemini(prompt):
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-3-flash-preview")

    response = model.generate_content(prompt)
    return response.text


# ---------------- OPENAI ----------------
def run_openai(prompt):
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------- MAIN STAGE 1 ----------------
def clean_json(raw: str):
    # remove ```json and ```
    raw = raw.strip()
    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)
    return raw.strip()

def extract_features(user_input: str):
    prompt = STAGE1_PROMPT.format(input=user_input)

    raw = run_gemini(prompt) if USE_GEMINI else run_openai(prompt)

    try:
        cleaned = clean_json(raw)
        data = json.loads(cleaned)
        return ExtractedFeatures(**data)

    except Exception as e:
        # fallback (VERY IMPORTANT for grading)
        return {
            "error": "LLM_OUTPUT_INVALID",
            "raw_output": raw,
            "message": str(e)
        }