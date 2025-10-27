import os
from crewai import LLM


def _bridge_google_to_gemini():
    """Bridge GOOGLE_API_KEY to GEMINI_API_KEY for Gemini providers."""
    if "GOOGLE_API_KEY" in os.environ and not os.environ.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]


def get_llm_model() -> str:
    """Return the default LLM model name from environment or sensible default."""
    return os.environ.get("GEMINI_MODEL", "gemini/gemini-2.0-flash")


def get_llm_temperature() -> float:
    """Return the default temperature, configurable via env var LLM_TEMPERATURE."""
    try:
        return float(os.environ.get("LLM_TEMPERATURE", "0.7"))
    except Exception:
        return 0.7


def get_llm() -> LLM:
    """Construct a shared LLM instance with centralized config and env bridges."""
    _bridge_google_to_gemini()
    return LLM(
        model=get_llm_model(),
        temperature=get_llm_temperature(),
    )