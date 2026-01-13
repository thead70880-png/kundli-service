import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseModel):
    """
    Centralized application configuration.
    """
    service_name: str = "kundli-service"
    environment: str = os.getenv("ENVIRONMENT", "development")
    opencage_api_key: str


def get_settings() -> Settings:
    api_key = os.getenv("OPENCAGE_API_KEY")

    if not api_key:
        raise RuntimeError("OPENCAGE_API_KEY is missing. Backend cannot start.")

    return Settings(opencage_api_key=api_key)


settings = get_settings()
