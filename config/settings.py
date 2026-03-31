from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "adaptive-content-dag"
    env: str = "local"
    log_level: str = "INFO"
    redis_url: str = "redis://redis:6379/0"
    lancedb_path: str = "data/lancedb"
    groq_api_key: str = ""
    groq_model: str = "llama3-70b-8192"
    groq_temperature: float = 0.4
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    langsmith_enabled: bool = False
    langsmith_api_key: str = ""
    langsmith_project: str = "adaptive-content-dag"
    llm_max_retries: int = 3
    llm_retry_base_delay: float = 1.5
    llm_retry_max_delay: float = 8.0
    fast_mode: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
