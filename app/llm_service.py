"""
LLM service: generate natural-language weather prediction using forecast data + RAG context.
Uses OpenAI if OPENAI_API_KEY is set; otherwise returns a structured template response (no key).
"""

import os
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


SYSTEM_PROMPT = """You are a helpful weather assistant. Given forecast data (maximum/minimum temperature and relative humidity) for a location, you provide a clear, concise summary and interpretation.

Use the following RETRIEVED CONTEXT only to add brief, relevant tips (e.g., comfort, humidity interpretation). Do not make up numbers—use only the FORECAST DATA provided.

Format your response in a friendly, readable way. Always include:
1. Location name.
2. For the next 1–2 days: maximum temperature, minimum temperature, and relative humidity (from the data).
3. A short interpretation (e.g., how it might feel, any tip from context if relevant).

Keep the response under 200 words unless the user asked for more detail."""

USER_TEMPLATE = """RETRIEVED CONTEXT (use only for tips/interpretation):
{context}

FORECAST DATA (use these numbers only):
{forecast_text}

Location: {location_name}
User query: zipcode {zipcode} — predict maximum and minimum temperature and relative humidity."""


def _format_forecast(forecast: dict, location_name: str, days: int = 2) -> str:
    """Turn forecast dict into a short text block for the prompt."""
    if not forecast:
        return "No forecast data available."
    lines = [f"Location: {location_name}", ""]
    times = forecast.get("time") or []
    t_min = forecast.get("temperature_min") or []
    t_max = forecast.get("temperature_max") or []
    rh = forecast.get("relative_humidity_mean") or []
    for i in range(min(days, len(times))):
        date = times[i] if i < len(times) else "N/A"
        mn = t_min[i] if i < len(t_min) else "N/A"
        mx = t_max[i] if i < len(t_max) else "N/A"
        h = rh[i] if i < len(rh) else "N/A"
        lines.append(f"Day {i+1} ({date}): Min temp: {mn}°C, Max temp: {mx}°C, Mean relative humidity: {h}%")
    return "\n".join(lines)


def get_llm():
    """Return OpenAI chat model if API key is set; otherwise None (use template fallback)."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if api_key:
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=api_key)
    return None


def generate_response(
    zipcode: str,
    location_name: str,
    forecast: dict,
    context: str,
    llm=None,
) -> str:
    """Generate final answer: max/min temp and relative humidity prediction + interpretation."""
    forecast_text = _format_forecast(forecast, location_name, days=2)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", USER_TEMPLATE),
    ])
    if llm is None:
        llm = get_llm()
    if llm is not None:
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({
            "context": context or "No additional context.",
            "forecast_text": forecast_text,
            "location_name": location_name,
            "zipcode": zipcode,
        })
    # Fallback: no API key — return structured summary without LLM
    lines = [
        f"**Location:** {location_name} (zipcode: {zipcode})",
        "",
        "**Forecast (next 2 days):**",
        forecast_text,
        "",
        "*(Set OPENAI_API_KEY in .env for an LLM-generated interpretation and tips.)*",
    ]
    return "\n".join(lines)
