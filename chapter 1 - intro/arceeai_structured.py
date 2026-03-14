#this code shows how to use ARCEEAI model 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, List
import os 


load_dotenv()

class Country(BaseModel):
    name: str = Field(description="The country name")
    description:str = Field(description="Brief description about the country")
    population: Optional[int]  = Field(default= None, description="population of the country")

llm = ChatOpenAI(
    api_key=os.environ.get("ARCEE_API_KEY"),
    model="arcee-ai/trinity-large-preview:free",
    base_url ="https://openrouter.ai/api/v1",

    temperature=0.4,
)
structured_llm = llm.with_structured_output(Country)

country = structured_llm.invoke("List the countries under United Kingdom")

# print(response.content)
print(f"Country: {country.name}\nDescription:\n{country.description}\nPopulation: {country.population}")
