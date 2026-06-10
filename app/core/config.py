from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "SI AI Service"
    app_env: str = "development"
    log_level: str = "info"
    api_prefix: str = "/api/v1"

    internal_api_key: str
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    llm_provider: str = "groq"
    llm_max_tokens: int = 1024
    llm_temperature: float = 0.4

    cors_origins: str = "http://localhost:3000,http://localhost:4000"


settings = Settings()
