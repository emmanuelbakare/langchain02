from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from  typing import List
import json
from dotenv import load_dotenv

load_dotenv()

class ProductReview(BaseModel):
    """Structured Product Review Analysis"""
    product_name:str = Field(description="Name of the Product")
    sentiments: str = Field(description="OVerall sentiment: Positive, Negative , Neutral")
    rating:int = Field(description="Ratings from 1 to 5", ge=1, le=5)
    pros:List[str] = Field(description="List of positive aspect")
    cons:List[str] = Field(description="List of negative aspect")
    summary:str = Field(description="Brief summary of review")

llm = ChatOpenAI(model="gpt-4o")
structured_llm = llm.with_structured_output(ProductReview)

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a product review analyzer. Extract strctured information from reviews"),
    ("user","{review_message}")
])

review_message =  input("Enter Review:")

chain =  prompt | structured_llm 

result = chain.invoke({
    "review_message":review_message
})

print(json.dumps( result.model_dump(), indent=2))