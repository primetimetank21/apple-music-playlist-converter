from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # SPOTIFY_CLIENT_ID: str
    # SPOTIFY_CLIENT_SECRET: str
    # SPOTIFY_REDIRECT_URI: str
    SCOPE: str | list[str] = Field(default="", alias="SCOPE")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("SCOPE")
    @classmethod
    def validate_scope(cls, v: str | list[str]) -> str | list[str]:
        if isinstance(v, str):
            # Convert comma-separated string to list
            return [scope.strip() for scope in v.split(",")]
        return v


settings = Settings()
