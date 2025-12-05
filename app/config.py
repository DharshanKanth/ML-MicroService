from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ML Prediction API"
    APP_VERSION: str = "1.0.0"
    MODEL_PATH: str = "iris_model.joblib"

    class Config:
        env_file = ".env"
settings=Settings()