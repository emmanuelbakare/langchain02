from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(model="gpt-4o")

response = llm.invoke("Tell me about NNPC in Nigeria")

# 1. get usage data
# print(response.usage_metadata)

#2. get usage data from response_metadata
print(response.response_metadata["token_usage"])