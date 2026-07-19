from state import AuditState
from services.base_llm import BaseLLM
import json

class CriticAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def run(self, state: AuditState) -> dict:
        print("--- АГЕНТ: КРИТИК (проверяет ревьюера...) ---")
        
        code = state.get("code_snippet", "")
        review = state.get("agent_review", "")
        rules = state.get("retrieved_rules", "")
        current_iterations = state.get("iteration_count", 0) + 1

        # Если превысили лимит итераций, принудительно завершаем
        if current_iterations >= 3:
            print("Критик: Достигнут лимит итераций, завершаем.")
            return {
                "needs_revision": False,
                "iteration_count": current_iterations
            }

        prompt = f"""
Ты старший инженер по безопасности (AppSec Lead).
Твоя задача - проверить отчет младшего ревьюера (AppSec Engineer).

Исходный код:
```cpp
{code}
```

Справочник уязвимостей (CWE), который был доступен ревьюеру:
{rules}

Отчет ревьюера:
{review}

Твоя задача:
1. Проверить, не выдумал ли ревьюер уязвимости или CWE (галлюцинации).
2. Проверить, действительно ли код содержит описанные проблемы.
3. Если отчет отличный и точный — согласиться.
4. Если есть ошибки (выдуманные CWE, ложные срабатывания) — отправить на доработку.

Ответь строго в формате JSON:
{{
    "needs_revision": true/false,
    "feedback": "Краткий комментарий для ревьюера, что исправить. Если всё ок, оставь пустым."
}}
"""
        response_text = self.llm.invoke(prompt)
        
        # Пытаемся распарсить JSON из ответа модели
        try:
            # Ищем начало и конец JSON (иногда модель пишет текст до/после JSON)
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                needs_rev = result.get("needs_revision", False)
                feedback = result.get("feedback", "")
            else:
                needs_rev = False
                feedback = "Не удалось распарсить ответ."
        except json.JSONDecodeError:
            needs_rev = False
            feedback = "Ошибка JSON."

        if needs_rev:
            print(f"Критик: Ревьюер ошибся! Отправляю на доработку. Комментарий: {feedback}")
            # Возвращаем обновленный отзыв (чтобы ревьюер знал, что исправить)
            return {
                "needs_revision": True,
                "iteration_count": current_iterations,
                "agent_review": f"{review}\n\n[ЗАМЕЧАНИЕ КРИТИКА: {feedback}. Исправь отчет!]"
            }
        else:
            print("Критик: Отчет принят, все отлично!")
            return {
                "needs_revision": False,
                "iteration_count": current_iterations
            }
