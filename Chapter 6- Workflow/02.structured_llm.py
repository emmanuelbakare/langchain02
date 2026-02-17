# implement structured output
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
import json 
from dotenv import load_dotenv

load_dotenv()

class ProductReview(BaseModel):
    """Structured product review analysis"""
    product_name: str = Field(description="Name of the product")
    sentiments:str = Field(description="Overall sentiment: positive, negative or neutral")
    rating: int = Field(description="Rating from 1-5", ge=1, le=5)
    pros: List[str] = Field(description="List of positive aspect")
    cons: List[str] = Field(description="List of negative aspect")
    summary:str = Field(description="Brief summary of review")

llm = ChatOpenAI(model="gpt-4o")

structured_llm = llm.with_structured_output(ProductReview)


prompt = ChatPromptTemplate.from_messages([
    #use tuple like this
    ("system"," You are a product review analyzer. Extract strctured information from reviews"),
    ("user", "{review_text}")

    #or use dictionary like this
    # {"role":"system","content":" You are a product review analyzer. Extract strctured information from reviews"},
    # {"role":"user","content":"{review_text}"}
])

chain = prompt | structured_llm
review_text = """ I bought this wireless mouse last month and its been mostly greay.
The battery life is incredible- I've only charged it onces in 4 weeks.
The ergonomic design fits my hand perfectly and the buttons are responsive.
However, the scroll wheel is a bit stiff and makes clicking sounds.
Alsp, it's quite expensitve comared to similar models.
Overall, i'd give it a 4 out of 5 stars
"""

result = chain.invoke ({
    "review_text": review_text
})

print(json.dumps(result.model_dump(), indent = 2))