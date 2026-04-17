from fastapi import FastAPI
from api.routes import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Real Estate Agent",
    description="LLM + ML prompt chaining system",
    version="1.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)