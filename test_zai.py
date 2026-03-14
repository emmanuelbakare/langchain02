from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

load_dotenv()

llm = ChatOpenAI(
    model="glm-5.2",
    api_key=os.getenv("ZAI_API_KEY"),
    base_url="https://api.z.ai/api/paas/v4/",
    temperature=0.6,
)

response = llm.invoke([
    SystemMessage(content="You are a helpful software engineering assistant."),
    HumanMessage(content="Explain LangChain RAG in simple terms.")
])

print(response.content)