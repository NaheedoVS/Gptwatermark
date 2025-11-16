from pydantic import BaseSettings


class Settings(BaseSettings):
BOT_TOKEN: str
API_ID: int
API_HASH: str
MONGO_URI: str | None = None
LOG_CHANNEL: str | None = None
UPLOAD_THRESHOLD_MB: int = 1900
DEFAULT_PRESET: str = "superfast"
DEFAULT_CRF: int = 23


class Config:
env_file = ".env"


settings = Settings()
