from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


model  = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("Write a short sentence about {topic}")

outputParser = StrOutputParser()

simple_chain = prompt | model | outputParser

result = simple_chain.invoke({"topic":"Football"})

print(result)

#demo 2 Chain to Runnable
combined_chain = simple_chain | (lambda input: input + "\n That is a great result")

result  = combined_chain.invoke("Digital Marketing")
print(result)