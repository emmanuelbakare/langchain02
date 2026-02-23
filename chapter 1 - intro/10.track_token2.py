#this code calculate the total cost of the token used and also show the input and output tokens used
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

"""
Output:
Tokens Used: 467
        Prompt Tokens: 27
                Prompt Tokens Cached: 0
        Completion Tokens: 440
                Reasoning Tokens: 0
Successful Requests: 2
Total Cost (USD): $0.0044675
"""