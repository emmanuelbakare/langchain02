from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-pro"
)

response = llm.invoke("Write a Short Poem about AI")
print(response.content)