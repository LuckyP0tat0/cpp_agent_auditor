import requests
from services.base_llm import BaseLLM

class OllamaLLM(BaseLLM):

    def __init__(self, model_name: str = "llama3", temperature: float = 0.1):
        self.model_name = model_name
        self.temperature = temperature
        self.base_url = "http://localhost:11434"
    
    def invoke(self, prompt:str) -> str:
        
        payload ={
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": self.temperature}
        }
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
