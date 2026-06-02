from __future__ import annotations

from urllib.parse import urlparse, urlunparse

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    app_env: str = "development"
    app_secret_key: str = "dev-secret-change-me"
    redis_url: str = "redis://127.0.0.1:6379/0"

    public_web_url: str = "http://localhost:3000"
    public_api_url: str = "http://localhost:8000"
    next_allowed_dev_origins: str = ""

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4.1-mini"

    cors_extra_origins: list[str] = Field(default_factory=list)

    @property
    def cors_origins(self) -> list[str]:
        origins = {
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            self.public_web_url,
        }
        parsed_web_url = urlparse(self.public_web_url)
        if parsed_web_url.hostname == "localhost":
            origins.add(urlunparse(parsed_web_url._replace(netloc=parsed_web_url.netloc.replace("localhost", "127.0.0.1"))))
        elif parsed_web_url.hostname == "127.0.0.1":
            origins.add(urlunparse(parsed_web_url._replace(netloc=parsed_web_url.netloc.replace("127.0.0.1", "localhost"))))
        if self.next_allowed_dev_origins:
            origins.add(self.next_allowed_dev_origins)
        origins.update(self.cors_extra_origins)
        return sorted(origin for origin in origins if origin)


settings = Settings()
