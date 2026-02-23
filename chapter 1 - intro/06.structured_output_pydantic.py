from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


# llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm = ChatOpenAI(model="gpt-5.2")

class President(BaseModel):
    """ Details about the president of a country"""
    name: str = Field(description="name of the president")
    country:str = Field(description="Country of the President")
    age: Optional[int] = Field(default=None, description="Age of the President")


structured_llm = llm.with_structured_output(President)

response=structured_llm.invoke("Who is the president of the USA")
print(response)
"""
Output:
gpt-4o (uses old data)
name='Joe Biden' country='United States of America' age=80

gpt-5.2 (uses current data)
name='Donald Trump' country='United States' age=None
"""