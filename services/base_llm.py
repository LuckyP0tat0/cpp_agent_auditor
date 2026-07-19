from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Абстрактный интерфейс для любой LLM."""
    @abstractmethod
    def invoke(self, prompt: str)-> str:
        """Отправить запрос в LLM и получить строку-ответ."""
        ...