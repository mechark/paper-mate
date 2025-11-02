from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_BASE_URL: str
    MODEL_NAME: str

    # Model parameters
    MODEL_MAX_TOKENS: int = 512
    MODEL_TEMPERATURE: float = 0.7

    # Retriever parameters
    RETRIEVER_K_BEFORE_RERANK: int = 80
    RETRIEVER_K_AFTER_RERANK: int = 4
    RETRIEVER_K_CONSTANT: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
