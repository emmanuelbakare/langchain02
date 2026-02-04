from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(model="gpt-4o", temperature=0)

class President(BaseModel):
    """ Details about the president of a country"""
    name: str = Field(description="name of the president")
    country:str = Field(description="Country of the President")
    age: Optional[int] = Field(default=None, description="Age of the President")


structured_llm = llm.with_structured_output(President)

response=structured_llm.invoke("Who is the president of the USA")
print(response)