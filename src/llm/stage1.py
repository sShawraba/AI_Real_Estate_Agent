import os
import re
import json
from dotenv import load_dotenv
from src.llm.schemas import ExtractedFeatures
from src.llm.prompts import STAGE1_PROMPT
from functools import lru_cache

# Load environment variables from .env file
load_dotenv()


USE_GEMINI = True  # switch anytime

# ---------------- GEMINI ----------------
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


# ---------------- OPENAI ----------------
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


# ---------------- MAIN STAGE 1 ----------------
QUAL_MAP = {
    "poor": 1,
    "fair": 3,
    "typical": 5,
    "average": 5,
    "good": 7,
    "very good": 8,
    "excellent": 10
}
def normalize_keys(data: dict):
    """Normalize keys: lowercase, remove extra spaces, apply quality mappings"""
    fixed = {}

    for k, v in data.items():
        key = k.lower().strip()
        key = key.replace(" ", "_")
        key = re.sub(r"_+", "_", key)  # remove multiple underscores

        # Map quality descriptors to numeric values
        if key == "overall_qual" and isinstance(v, str):
            v = QUAL_MAP.get(v.lower(), v)  # fallback to original if not found

        fixed[key] = v

    return fixed

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
        data = normalize_keys(data)  # 👈 ADD THIS

        return ExtractedFeatures(**data)

    except Exception as e:
        # fallback
        return {
            "error": "LLM_OUTPUT_INVALID",
            "raw_output": raw,
            "message": str(e)
        }
    

# # like what we did in class
# @lru_cache(maxsize=1)
# def _get_gemini_client():
#     from google import genai
#     return genai.Client(api_key=GEMINI_API_KEY)


# @lru_cache(maxsize=1)
# def _get_openai_client():
#     from openai import OpenAI
#     return OpenAI(api_key=OPENAI_API_KEY)

# def call_llm_structured(user_prompt: str, response_model: type[BaseModel], system_prompt: str = "") -> BaseModel:
#     """
#     Send a prompt to the LLM and return a validated Pydantic model.

#     Uses provider-native structured output to guarantee the response
#     conforms to the schema. No manual JSON parsing needed.
#     """
#     if LLM_PROVIDER == "gemini":
#         return _call_gemini_structured(user_prompt, response_model, system_prompt)
#     if LLM_PROVIDER == "openai":
#         return _call_openai_structured(user_prompt, response_model, system_prompt)
#     return _call_azure_structured(user_prompt, response_model, system_prompt)

# def _call_gemini_structured(user_prompt: str, response_model: type[BaseModel], system_prompt: str) -> BaseModel:
#     """Call Gemini with native structured output via response_schema."""
#     from google.genai import types

#     client = _get_gemini_client()

#     config = types.GenerateContentConfig(
#         temperature=0.3,
#         response_mime_type="application/json",
#         response_schema=response_model,
#     )
#     if system_prompt:
#         config.system_instruction = system_prompt

#     response = client.models.generate_content(
#         model=GEMINI_MODEL,
#         contents=user_prompt,
#         config=config,
#     )

#     return response_model.model_validate_json(response.text)

# def _call_openai_structured(user_prompt: str, response_model: type[BaseModel], system_prompt: str) -> BaseModel:
#     """Call OpenAI with native structured output via response_format."""
#     client = _get_openai_client()

#     messages = []
#     if system_prompt:
#         messages.append({"role": "system", "content": system_prompt})
#     messages.append({"role": "user", "content": user_prompt})

#     response = client.beta.chat.completions.parse(
#         model=OPENAI_MODEL,
#         messages=messages,
#         temperature=0.3,
#         response_format=response_model,
#     )

#     return response.choices[0].message.parsed