from state import AuditState
from services.base_llm import BaseLLM

class ReviewerAgent:
    def __init__(self, llm: BaseLLM):
        """
        Агент принимает любую LLM, которая соответствует контракту BaseLLM.
        """
        self.llm = llm

    def run(self, state: AuditState) -> dict:
        """
        Метод, который будет вызываться графом.
        Принимает текущее состояние, возвращает словарь с обновлениями.
        """
        code = state.get("code_snippet", "")
        
        # 1. Формируем промпт (запрос) для нейросети
        prompt = f"""
Ты эксперт по безопасности C++ кода (AppSec Engineer).
Твоя задача - проанализировать следующий код на наличие уязвимостей (CWE, утечки памяти, buffer overflow и т.д.).

КОД ДЛЯ АНАЛИЗА:
```cpp
{code}
```

Напиши краткий отчет на русском языке: какие уязвимости найдены и как их исправить.
Если уязвимостей нет, напиши "Код безопасен".
"""
        
        print("--- АГЕНТ: РЕВЬЮЕР (вызывает LLM...) ---")
        
        # 2. Отправляем запрос в LLM
        review_result = self.llm.invoke(prompt)
        
        print("--- АГЕНТ: РЕВЬЮЕР (ответ получен) ---")
        
        # 3. Возвращаем только то поле, которое мы изменили
        return {"agent_review": review_result}
