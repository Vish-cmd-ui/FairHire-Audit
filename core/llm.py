"""
core/llm.py - Shared LLM Client with Persistent Caching & Fallback

Features:
- Configurable model, base URL, and API key via .env
- SHA-256 caching of (model + prompt) in cache.json
- Deterministic temperature=0.0
- Auto-fallback across models on token rate limits (TPD)
"""

import os
import json
import time
import hashlib
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
CACHE_FILE = "cache.json"


def _get_env_config():
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    model = os.getenv("LLM_MODEL", "openai/gpt-oss-20b")

    if not api_key or api_key in ("your-api-key-here", "gsk_your_groq_api_key_here", ""):
        raise ValueError("Missing or invalid LLM_API_KEY in .env file.")
    return api_key, base_url, model


def _compute_cache_key(model: str, prompt: str) -> str:
    combined = f"{model}:{prompt}"
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


def _load_cache() -> dict:
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(cache: dict) -> None:
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Warning] Failed to write to cache.json: {e}")


def ask(prompt: str, max_retries: int = 3, retry_delay_seconds: float = 2.0) -> str:
    api_key, base_url, model = _get_env_config()

    cache = _load_cache()
    cache_key = _compute_cache_key(model, prompt)

    if cache_key in cache:
        return cache[cache_key]

    client = OpenAI(api_key=api_key, base_url=base_url)

    fallback_models = [model]
    if "openai/gpt-oss-20b" not in fallback_models:
        fallback_models.append("openai/gpt-oss-20b")
    if "qwen/qwen3.8-27b" not in fallback_models:
        fallback_models.append("qwen/qwen3.8-27b")

    last_error: Optional[Exception] = None

    for current_model in fallback_models:
        fb_cache_key = _compute_cache_key(current_model, prompt)
        if fb_cache_key in cache:
            return cache[fb_cache_key]

        for attempt in range(1, max_retries + 1):
            try:
                response = client.chat.completions.create(
                    model=current_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                )
                answer = response.choices[0].message.content or ""

                cache[cache_key] = answer
                cache[fb_cache_key] = answer
                _save_cache(cache)
                return answer

            except Exception as err:
                last_error = err
                err_msg = str(err).lower()
                if "tokens per day" in err_msg or "daily" in err_msg or "tpd" in err_msg:
                    print(f"[Fallback] Daily limit reached on {current_model}. Switching...")
                    break
                if attempt < max_retries:
                    time.sleep(retry_delay_seconds)

    raise RuntimeError(f"Failed to get LLM response after attempts: {last_error}")
