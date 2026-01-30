"""
RAG pipeline: zipcode -> weather API -> RAG context -> LLM prediction (max/min temp, humidity).
"""

from typing import Optional

from app.weather_service import get_weather_for_zipcode
from app.rag_service import load_and_index_knowledge, retrieve_context
from app.llm_service import generate_response, get_llm


def predict(zipcode: str, country: str = "US", use_rag: bool = True) -> dict:
    """
    Run the full RAG pipeline for a zipcode.
    Returns dict with keys: success, message, location, forecast (raw), error.
    """
    result = get_weather_for_zipcode(zipcode, country)
    if result.get("error"):
        return {
            "success": False,
            "message": result["error"],
            "location": result.get("location"),
            "forecast": result.get("forecast"),
            "error": result["error"],
        }
    location = result["location"]
    forecast = result["forecast"]
    location_name = location.get("name", zipcode)

    context = ""
    if use_rag:
        try:
            vectorstore = load_and_index_knowledge()
            query = f"temperature humidity forecast maximum minimum relative humidity {zipcode}"
            context = retrieve_context(query, vectorstore, k=4)
        except Exception as e:
            context = f"(RAG retrieval failed: {e})"

    message = generate_response(
        zipcode=zipcode,
        location_name=location_name,
        forecast=forecast,
        context=context,
        llm=get_llm(),
    )

    return {
        "success": True,
        "message": message,
        "location": location,
        "forecast": forecast,
        "error": None,
    }
