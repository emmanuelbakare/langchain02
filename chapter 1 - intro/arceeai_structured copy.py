#this code shows how to use ARCEEAI model 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, List
from langchain_openai import ChatOpenAI
import os 


load_dotenv()

class Country(BaseModel):
    name: str = Field(description="The country name")
    description:str = Field(description="Brief description about the country")
    population: Optional[int]  = Field(default= None, description="population of the country")

class CountryList(BaseModel):
    countries:List[Country] = Field(description="List of Countries with their details")
    summary: str = Field(description="brief overall summary of the result")
llm = ChatOpenAI(
    api_key=os.environ.get("ARCEE_API_KEY"),
    model="arcee-ai/trinity-large-preview:free",
    base_url ="https://openrouter.ai/api/v1",

    temperature=0.4,
)
# llm = ChatOpenAI(model="gpt-4o")

structured_llm = llm.with_structured_output(CountryList)

response = structured_llm.invoke("List the countries under United Kingdom")

# print(countries)
for country in response.countries:
    print(f"Country: {country.name}\nDescription:\n{country.description}\nPopulation: {country.population}\n\n")

print("Summary:\n", response.summary)