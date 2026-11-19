from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    SECRET_KEY: str
    DATABASE_URL: str = "sqlite:///./dev.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGIN: list[str] = ["http://localhost:5173"]

    @field_validator("SECRET_KEY")
    @classmethod
    def secret_must_be_strong(cls, v: str) -> str:
        if len(v) < 32 or v == "change-me":
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v

settings = Settings()
