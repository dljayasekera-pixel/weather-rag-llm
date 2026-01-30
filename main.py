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
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.predict import predict as run_predict

PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_ROOT / "static"

app = FastAPI(
    title="Weather RAG LLM",
    description="Predict maximum/minimum temperature and relative humidity for a zipcode using RAG + LLM.",
    version="1.0.0",
)

# Serve static assets (CSS, JS)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ZipcodeRequest(BaseModel):
    zipcode: str
    country: str = "US"


class PredictionResponse(BaseModel):
    success: bool
    message: str
    location: dict | None
    forecast: dict | None
    error: str | None


@app.get("/health")
def health():
    """Lightweight health check for Render (no RAG load)."""
    return {"status": "ok"}


@app.get("/")
def root():
    """Serve the website (zipcode form)."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"service": "Weather RAG LLM", "docs": "/docs", "predict": "POST /predict"}


@app.post("/predict", response_model=PredictionResponse)
def api_predict(req: ZipcodeRequest):
    """Predict max/min temperature and relative humidity for the given zipcode."""
    zipcode = (req.zipcode or "").strip()
    if not zipcode:
        raise HTTPException(status_code=400, detail="zipcode is required")
    try:
        result = run_predict(zipcode=zipcode, country=req.country or "US", use_rag=True)
    except Exception as e:
        return PredictionResponse(
            success=False,
            message=f"Server error: {str(e)}",
            location=None,
            forecast=None,
            error=str(e),
        )
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
