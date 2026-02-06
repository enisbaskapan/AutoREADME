import os
from typing import Literal
from langchain_openai import ChatOpenAI


class LLM:

    def __init__(self, provider: Literal["openai", "groq", "claude"] = "groq") -> None:
        self.provider = provider
        self.base_urls = {
            "openai": "https://api.openai.com/v1",
            "groq": "https://api.groq.com/openai/v1",
            "claude": "https://api.anthropic.com/v1/",
        }

    def get_model(self, model_name: str, temperature: float = 0.5) -> ChatOpenAI:
        api_key_env = {
            "openai": "OPENAI_API_KEY",
            "groq": "GROQ_API_KEY",
            "claude": "ANTHROPIC_API_KEY",
        }

        api_key = os.getenv(api_key_env[self.provider])
        if not api_key:
            raise ValueError(f"Missing API key for provider: {self.provider}")

        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key,
            base_url=self.base_urls[self.provider],
        )
