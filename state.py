from typing_extensions import TypedDict

class AuditState(TypedDict):
    code_snippet: str      # Исходный код C++, который проверяем
    retrieved_rules: str   # Правила безопасности (например, MISRA C++ или CWE)
    agent_review: str      # Результат анализа первого агента-ревьюера
    needs_revision: bool   # Логический флаг от критика (нужна ли доработка)
    iteration_count: int   # Счётчик итераций, чтобы не зациклиться