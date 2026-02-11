import os
from typing import Any, List, Optional, Mapping
from pydantic import Field
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_ollama import ChatOllama
from tenacity import retry, stop_after_attempt, wait_exponential
from strike_crew.config import OllamaLLMConfig

class CustomOllamaLLM(BaseChatModel):
    """Custom Ollama LLM wrapper with retry logic and error handling."""

    config: OllamaLLMConfig = Field(default_factory=OllamaLLMConfig)
    chat_model: Optional[ChatOllama] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, config: OllamaLLMConfig, **data: Any):
        super().__init__(**data)
        self.config = config
        self.chat_model = self._create_chat_model()

    def _create_chat_model(self) -> ChatOllama:
        """Create ChatOllama instance with configuration."""
        return ChatOllama(
            model=self.config.model_name,
            temperature=self.config.temperature,
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any
    ) -> ChatResult:
        """Generate response with retry logic for connection failures."""
        try:
            response = self.chat_model.invoke(messages, stop=stop, **kwargs)
            return ChatResult(generations=[ChatGeneration(message=response)])
        except ConnectionError as e:
            print(f"Connection error to Ollama: {e}. Retrying...")
            raise
        except Exception as e:
            print(f"Error during generation: {e}")
            raise

    def _llm_type(self) -> str:
        return "custom_ollama_llm"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            "model_name": self.chat_model.model,
            "temperature": self.chat_model.temperature,
            "base_url": self.config.base_url
        }
