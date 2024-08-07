import os
from typing import Any, List, Optional, Mapping
from pydantic import BaseModel, Field
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_groq import ChatGroq
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from groq import InternalServerError
from strike_crew.config import GroqLLMConfig

class GroqLLMConfig(BaseModel):
    temperature: float = 0
    model_name: str = "mixtral-8x7b-32768"
    model_config['protected_namespaces'] = ()

class CustomGroqLLM(BaseChatModel):
    config: GroqLLMConfig
    chat_model: Optional[ChatGroq] = None
    api_keys: List[str] = []
    current_key_index: int = 0

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, config: GroqLLMConfig):
        super().__init__(config=config)
        self.api_keys = self._load_api_keys()
        self.chat_model = self._create_chat_model()

    def _load_api_keys(self) -> List[str]:
        keys = []
        for i in range(1, 6):  # Assuming a maximum of 5 API keys
            key = os.getenv(f"GROQ_API_KEY_{i}")
            if key:
                keys.append(key)
        if not keys:
            raise ValueError("No Groq API keys found in environment variables.")
        return keys

    def _create_chat_model(self) -> ChatGroq:
        return ChatGroq(
            temperature=self.config.temperature, 
            model_name=self.config.model_name,
            groq_api_key=self.api_keys[self.current_key_index]
        )

    def _switch_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.chat_model = self._create_chat_model()
        print(f"Switched to API key {self.current_key_index + 1}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(InternalServerError)
    )
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, run_manager: Optional[Any] = None, **kwargs: Any) -> ChatResult:
        try:
            response = self.chat_model.invoke(messages, stop=stop, **kwargs)
            return ChatResult(generations=[ChatGeneration(message=response)])
        except InternalServerError as e:
            print(f"Encountered an internal server error: {e}. Switching API key and retrying...")
            self._switch_api_key()
            raise  # This will trigger the retry with the new API key

    def _llm_type(self) -> str:
        return "custom_groq_llm"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model_name": self.chat_model.model_name, "temperature": self.chat_model.temperature}