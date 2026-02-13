from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini")

#Demo 1 Invomced Prompt
invoked_prompt = "Where is the Eifefel tower"

response = llm.invoke(invoked_prompt)
print(f"----Invoked Prompt - Query: {invoked_prompt}")
print(response.content)
print("="*50)

#Demo 2 - Batched Prompt
batched_prompt = [
    "Is pineaple a fruit or a vegetable",
    "When was snow white first produced",
    "Who is the strongest wizard in Harry Porter?"
]

batched_response = llm.batch(batched_prompt)
print(f"----Invoked Prompt - Query: {invoked_prompt}")
for response in batched_response:
    print(f"{response.content}\n\n")

#Demo 3 - Streaming

stream_prompt = "Explain American Football"

streamed_response = llm.stream(stream_prompt)

for chunk in streamed_response:
    print(chunk.content, end="", flush=True)
    # print(chunk.content, end="| ", flush=True)  # put a | between each token
    