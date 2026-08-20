from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Centralized configuration management using Pydantic.
    Validates that required environment variables exist at startup.
    """
    PROJECT_NAME: str = "Nourient Food Intelligence"
    ENVIRONMENT: str = "development"
    
    # AI Credentials
    GEMINI_API_KEY: str
    
    # Firebase Credentials (Optional for local dev if default credentials are used, but good to have explicit)
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Singleton instance to be imported across microservices
settings = Settings()
