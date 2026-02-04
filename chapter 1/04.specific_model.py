from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model = "gpt-4o",
    api_key= os.environ.get("OPENAI_API_KEY"),   
)

response = llm.invoke("Who is the president of France")
print(response.content)
