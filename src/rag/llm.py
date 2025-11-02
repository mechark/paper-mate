from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from src.prompts import SYSTEM_PROMPT
from src.core.config import settings


def get_chain():
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

    llm = OllamaLLM(
        model=settings.MODEL_NAME,
        base_url=settings.OLLAMA_BASE_URL,
        validate_model_on_init=True,
        temperature=settings.MODEL_TEMPERATURE,
        max_tokens=settings.MODEL_MAX_TOKENS,
    )

    return prompt | llm
