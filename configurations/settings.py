from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "content_tool"
    env: str = "development"
    debug: bool = True

    class Config:
        env_prefix = "APP_"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
