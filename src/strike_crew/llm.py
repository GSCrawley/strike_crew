from typing import Any, List, Optional, Mapping
from pydantic import BaseModel, Field
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_groq import ChatGroq

class GroqLLMConfig(BaseModel):
    temperature: float = 0
    model_name: str = "mixtral-8x7b-32768"

class CustomGroqLLM(BaseChatModel):
    config: GroqLLMConfig
    chat_model: ChatGroq

    def __init__(self, **kwargs):
        config = GroqLLMConfig(**kwargs)
        chat_model = ChatGroq(temperature=config.temperature, model_name=config.model_name)
        super().__init__(config=config, chat_model=chat_model)

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, run_manager: Optional[Any] = None, **kwargs: Any) -> ChatResult:
        response = self.chat_model.invoke(messages, stop=stop, **kwargs)
        return ChatResult(generations=[ChatGeneration(message=response)])

    def _llm_type(self) -> str:
        return "custom_groq_llm"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model_name": self.chat_model.model_name, "temperature": self.chat_model.temperature}
