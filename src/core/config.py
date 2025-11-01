from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_BASE_URL: str
    MODEL_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()