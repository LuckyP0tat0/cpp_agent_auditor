from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3", temperature =0.1)

response = llm.invoke("Привет! Ты готов анализировать C++ код ?")

print(response.content)

