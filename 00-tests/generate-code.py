from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-5.2-chat-latest")

prompt = """
create a reflection langgraph for fine tuning twitter post. let a node generate the tweet and another reflect and create a condition that check if the tweet generate is good enough, funny enough and can go viral on tweeter. grade the tweet - 1 is lowest 10 is highest-, if the tweet is below 8 then regenerate the tweet based on the recommendation from the reflection. If the tweet is up to 8 then end the generation. use Pydantic BaseModel to get structured output so that you can seperate the value for score from the feeback



Use recent langgraph documentation to implement it and make it as detailed as possible.

do not add a prefix or suffix to the response. Generate only the code.
"""
response = llm.invoke(prompt)

code = response.content
print("=========CODE==============\n\n",code)

with open('reflection2.py', 'w') as file:
    file.write(code)

