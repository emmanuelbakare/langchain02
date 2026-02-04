#this code shows how to use ARCEEAI model 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os 

load_dotenv()


llm = ChatOpenAI(
    api_key=os.environ.get("ARCEE_API_KEY"),
    model="arcee-ai/trinity-large-preview:free",
    base_url ="https://openrouter.ai/api/v1",

    temperature=0.4,
)

response = llm.invoke("List the countries under United Kingdom")

print(response.content)
