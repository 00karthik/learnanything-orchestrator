import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional

from crewai import LLM

_ENV_LOADED = False


def _load_env_file() -> None:
    """Load variables from a .env file if present and not already loaded."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    env_path = os.environ.get("LEARN_ANYTHING_ENV_PATH")
    if env_path:
        candidate = Path(env_path)
    else:
        candidate = Path(__file__).resolve().parents[2] / ".env"

    if candidate.exists():
        for line in candidate.read_text().splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            if not key:
                continue
            if key in os.environ:
                continue
            os.environ[key] = value.strip()

    _ENV_LOADED = True


def _bridge_google_to_gemini() -> None:
    """Bridge GOOGLE_API_KEY to GEMINI_API_KEY for Gemini providers."""
    if "GOOGLE_API_KEY" in os.environ and not os.environ.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]


def _normalize_agent_name(agent_name: Optional[str]) -> Optional[str]:
    if not agent_name:
        return None
    key = re.sub(r"[^0-9A-Za-z]+", "_", agent_name.strip().upper())
    return key.strip("_") or None


def _mode_defaults(mode: str) -> Dict[str, str]:
    """Return default provider/model/temperature for the configured mode."""
    if mode == "aws_bedrock":
        return {
            "provider": os.environ.get("BEDROCK_PROVIDER", "bedrock"),
            "model": os.environ.get("BEDROCK_MODEL", "anthropic.claude-3-haiku-20240307-v1:0"),
            "temperature": os.environ.get("BEDROCK_TEMPERATURE", "0.5"),
        }

    # Local Gemini mode (default)
    return {
        "provider": os.environ.get("LOCAL_LLM_PROVIDER", "gemini"),
        "model": os.environ.get("GEMINI_MODEL", "gemini/gemini-2.0-flash"),
        "temperature": os.environ.get("LLM_TEMPERATURE", "0.7"),
    }


def _get_agent_setting(agent_key: Optional[str], suffix: str, fallback: str) -> str:
    """Lookup a configuration value for an agent with sensible fallbacks."""
    if agent_key:
        agent_specific_key = f"{agent_key}_{suffix}"
        if agent_specific_key in os.environ and os.environ[agent_specific_key] != "":
            return os.environ[agent_specific_key]

    general_key = f"LLM_{suffix}"
    if general_key in os.environ and os.environ[general_key] != "":
        return os.environ[general_key]

    return fallback


def _coerce_float(value: str, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default


@lru_cache(maxsize=None)
def get_llm(agent_name: Optional[str] = None) -> LLM:
    """Construct an LLM instance, allowing per-agent overrides and multiple modes."""
    _load_env_file()
    mode = os.environ.get("LLM_MODE", "local").strip().lower() or "local"
    defaults = _mode_defaults(mode)
    agent_key = _normalize_agent_name(agent_name)

    model = _get_agent_setting(agent_key, "MODEL", defaults["model"])
    provider_value = _get_agent_setting(agent_key, "PROVIDER", defaults["provider"])
    provider = provider_value.strip() if isinstance(provider_value, str) else ""
    provider_normalized = provider.lower()
    temperature_raw = _get_agent_setting(agent_key, "TEMPERATURE", defaults["temperature"])
    temperature = _coerce_float(temperature_raw, _coerce_float(defaults["temperature"], 0.7))

    if provider_normalized == "gemini":
        _bridge_google_to_gemini()

    llm_kwargs = {
        "model": model,
        "temperature": temperature,
    }

    if provider and provider_normalized not in {"", "gemini", "default"}:
        llm_kwargs["provider"] = provider

    if mode == "aws_bedrock" and provider_normalized == "bedrock":
        region = _get_agent_setting(agent_key, "BEDROCK_REGION", os.environ.get("BEDROCK_REGION", ""))
        if region:
            llm_kwargs["region_name"] = region

    return LLM(**llm_kwargs)