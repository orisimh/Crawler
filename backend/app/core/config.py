# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
from dotenv import load_dotenv

# ✅ Load the .env file explicitly
# load_dotenv("/backend/.env")

class Settings(BaseSettings):
    """Application settings"""
    app_name: str
    version: str
    v: str
    debug: bool
    host: str
    port: int
    allowed_origins: str # CORS settings
    request_timeout: float # Request timeout settings
    secret_key: str
    algorithm: str
    access_token_expire_minutes : float
    deals_name_html: str
    # Website configurations
    websites: dict = {
        "fo1.altius.finance": {
            "base_url": "https://fo1.altius.finance",
            "test_username": "fo1_test_user@whatever.com",
            "test_password": "Test123!"
        },
        "fo2.altius.finance": {
            "base_url": "https://fo2.altius.finance",
            "test_username": "fo2_test_user@whatever.com",
            "test_password": "Test223!"
        }
    }


    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()