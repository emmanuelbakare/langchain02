from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(model="gpt-4o")

streamed_output = llm.stream("Tell me about NNPC in Nigeria")

for chunk in streamed_output:
    print(chunk.content, end="", flush=True)
    # print(chunk.content, end="|", flush=True) # use a pip to show the token outputs
