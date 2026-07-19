import chromadb
from chromadb.utils import embedding_functions
from RAG.base_retriever import BaseRetriever
from RAG.cwe_knowledge import CWE_RULES

class ChromaRetriever(BaseRetriever):
    def __init__(self):
        self.client = chromadb.Client()
        
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Создаем коллекцию и ПЕРЕДАЕМ ей embedding_function
        self.collection = self.client.get_or_create_collection(
            name="cwe_knowledge_base",
            embedding_function=self.ef
        )
        
        self._seed_database()

    def _seed_database(self):
        """Заполняет базу векторными представлениями правил"""
        documents = []
        ids = []
        
        for rule in CWE_RULES:
            
            text = f"{rule['id']}: {rule['name']}. {rule['description']}"
            documents.append(text)
            ids.append(rule['id'])
            
        self.collection.add(
            documents=documents,
            ids=ids
        )
        print("База знаний RAG успешно загружена!")
    def retrieve(self, query: str, n_results: int = 2) -> str:
        """Поиск самых релевантных правил по запросу (коду)"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # results["documents"] содержит найденные строки
        if not results["documents"] or not results["documents"][0]:
            return "Релевантные правила не найдены."
            
        # Склеиваем найденные правила в одну строку
        found_rules = "\n".join(results["documents"][0])
        return found_rules