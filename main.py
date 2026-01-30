"""
Weather RAG LLM: predict max/min temperature and relative humidity by zipcode.
Run: uvicorn main:app --reload   (API)
     python main.py 90210        (CLI)
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.predict import predict as run_predict

app = FastAPI(
    title="Weather RAG LLM",
    description="Predict maximum/minimum temperature and relative humidity for a zipcode using RAG + LLM.",
    version="1.0.0",
)


class ZipcodeRequest(BaseModel):
    zipcode: str
    country: str = "US"


class PredictionResponse(BaseModel):
    success: bool
    message: str
    location: dict | None
    forecast: dict | None
    error: str | None


@app.get("/")
def root():
    return {"service": "Weather RAG LLM", "docs": "/docs", "predict": "POST /predict"}


@app.post("/predict", response_model=PredictionResponse)
def api_predict(req: ZipcodeRequest):
    """Predict max/min temperature and relative humidity for the given zipcode."""
    zipcode = (req.zipcode or "").strip()
    if not zipcode:
        raise HTTPException(status_code=400, detail="zipcode is required")
    result = run_predict(zipcode=zipcode, country=req.country or "US", use_rag=True)
    return PredictionResponse(
        success=result["success"],
        message=result["message"],
        location=result.get("location"),
        forecast=result.get("forecast"),
        error=result.get("error"),
    )


def cli():
    """CLI: python main.py <zipcode> [country]"""
    args = sys.argv[1:]
    if not args:
        print("Usage: python main.py <zipcode> [country]")
        print("Example: python main.py 90210 US")
        sys.exit(1)
    zipcode = args[0]
    country = args[1] if len(args) > 1 else "US"
    result = run_predict(zipcode=zipcode, country=country, use_rag=True)
    if result["success"]:
        print(result["message"])
    else:
        print("Error:", result.get("error", result["message"]))
        sys.exit(1)


if __name__ == "__main__":
    cli()
