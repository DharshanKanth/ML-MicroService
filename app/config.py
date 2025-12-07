from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # App metadata
    APP_NAME: str = "ML Prediction API"
    APP_VERSION: str = "1.0.0"

    # Base directory of the app (absolute path)
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

    # Model directory (absolute path → safe for Docker, K8s, CI/CD)
    MODEL_DIR: str = os.path.join(BASE_DIR, "models")

    # Default model version
    DEFAULT_VERSION: str = "v1"
    # API Key for authentication
    API_KEY: str


    class Config:
        env_file = ".env"     # Load environment variables from .env file

settings = Settings()
