# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
model = ChatOpenAI(model="gpt-4o")

response =  model.invoke("Who is the president of Nigeria")

# print(response.response_metadata.get('token_usage'))
# print(response.usage_metadata)
print(response.content)