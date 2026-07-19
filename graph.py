from typing  import Literal
from langgraph.graph import StateGraph, START,END
from state import AuditState
from services.ollama_llm import OllamaLLM
from agents.reviewer import ReviewerAgent
from agents.critic import CriticAgent
from RAG.chroma_retriever import ChromaRetriever
from dataset import get_code_snippet

llm_service = OllamaLLM(model_name="llama3", temperature=0.1)
reviewer_agent = ReviewerAgent(llm=llm_service)
critic_agent = CriticAgent(llm=llm_service)
retriever_service = ChromaRetriever()

def retriever_node(state: AuditState) -> dict:
    print("--- АГЕНТ: РЕТРИВЕР (ищет релевантные правила CWE...) ---")
    code = state.get("code_snippet", "")
    rules = retriever_service.retrieve(query=code, n_results=2)
    print("--- АГЕНТ: РЕТРИВЕР (правила найдены) ---")
    return {"retrieved_rules": rules}

def should_continue(state:AuditState) -> Literal["reviewer", "__end__"]:
    if state["needs_revision"] and state['iteration_count'] <3:
        return 'reviewer'
    return "__end__"
    
workflow = StateGraph(AuditState)

workflow.add_node("retriever", retriever_node)
workflow.add_node("reviewer", reviewer_agent.run)
workflow.add_node("critic", critic_agent.run)

workflow.add_edge(START, "retriever")
workflow.add_edge("retriever", "reviewer")
workflow.add_edge("reviewer", "critic")

workflow.add_conditional_edges(
    "critic",
    should_continue,
    {
        "reviewer": "reviewer",  
        "__end__": END          
    }
)

app = workflow.compile()

# --- 4. ТЕСТОВЫЙ ЗАПУСК ---
if __name__ == "__main__":
    print("Запуск графа...")

    code = get_code_snippet()

    print("\n=== КОД ДЛЯ АНАЛИЗА ===")
    print(code)  # Первые 500 символов, чтобы не захламлять терминал
    print("...\n")

    initial_state = {
        "code_snippet": code,
        "iteration_count": 0
    }
    
    # Прогоняем граф через stream (видим промежуточные шаги)
    for output in app.stream(initial_state):
        for key, value in output.items():
            print(f"Узел '{key}' завершил работу.")
            # Если ревьюер прислал ответ — показываем его
            if "agent_review" in value:
                print("\n>>> ОТВЕТ РЕВЬЮЕРА:")
                print(value["agent_review"])
                print()
