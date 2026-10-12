from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1:8b"
)

response = llm.invoke("""
Target Production: 15000
Projected Production: 12750
Gap: 2250

Provide:
1. Status
2. Risk
3. Recommendation
""")

print(response.content)