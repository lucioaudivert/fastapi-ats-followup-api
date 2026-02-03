"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="ATS_",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
