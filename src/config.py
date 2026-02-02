import logging

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CLIENT_ID: str = Field(default="", alias="CLIENT_ID")
    CLIENT_SECRET: str = Field(default="", alias="CLIENT_SECRET")
    REDIRECT_URI: str = Field(default="", alias="REDIRECT_URL")
    LOG_LEVEL: int = Field(default=logging.INFO, alias="LOG_LEVEL")
    SCOPE: str | list[str] = Field(default="", alias="SCOPE")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("SCOPE")
    @classmethod
    def validate_scope(cls, v: str | list[str]) -> str | list[str]:
        if isinstance(v, str):
            # Convert comma-separated string to list
            return [scope.strip() for scope in v.split(",")]
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str | int) -> int:
        if isinstance(v, str):
            level_map: dict[str, int] = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL,
            }
            level: str = v.upper()
            return level_map.get(level, logging.INFO)
        if isinstance(v, int):
            level_map_int: dict[int, int] = {
                logging.DEBUG: logging.DEBUG,
                logging.INFO: logging.INFO,
                logging.WARNING: logging.WARNING,
                logging.ERROR: logging.ERROR,
                logging.CRITICAL: logging.CRITICAL,
            }
            return level_map_int.get(v, logging.INFO)


settings = Settings()
