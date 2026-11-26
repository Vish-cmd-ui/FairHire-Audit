"""
llm.py - Root wrapper for core.llm
"""
from core.llm import ask, _load_cache, _save_cache, _compute_cache_key, _get_env_config

if __name__ == "__main__":
    reply = ask("Say hello in 3 words")
    print("Response:", reply)
