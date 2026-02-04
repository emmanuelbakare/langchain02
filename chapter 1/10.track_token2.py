from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(model="gpt-4o")


with get_openai_callback() as callback:
    response1 = llm.invoke("Tell me about NNPC in Nigeria")
    response2 = llm.invoke("Who is the President of Nigeria")
    print(callback)
    # print(callback.total_cost)