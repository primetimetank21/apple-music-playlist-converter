from pathlib import Path
from typing import Final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

FRONTEND_ROOT: Final[Path] = Path(__file__).resolve().parents[1]  # "/src/frontend"


class Settings(BaseSettings):
    BACKEND_URL: str = Field(default="http://localhost:8000", alias="BACKEND_URL")
    FRONTEND_URL: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")

    model_config = SettingsConfigDict(
        env_file=Path(FRONTEND_ROOT, ".env"), env_file_encoding="utf-8"
    )


settings = Settings()
