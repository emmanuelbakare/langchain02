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

print(f"{result}")
print("*"*100)
 
 #Demo 2 2nd Chain
combined_chain = simple_chain | (lambda output: output + "Great Answer")

print("---Combined Chain Output----")
combined_chain_result = combined_chain.invoke({
    "topic":"Telephone"
})

print(combined_chain_result)

#demo 3 - Chain to chain combination

fact_checking_prompt = ChatPromptTemplate.from_messages([
    ("system","Start by quoting the statement, then give the reason"),
    ("user","How correct is this statement: {statement}")
])

checker_chain  = fact_checking_prompt | model | outputParser

fact_checking_chain = {"statement":simple_chain} | checker_chain

dual_chain_result = fact_checking_chain.invoke({
    "topic":"Prompt Engineering"
})

print("___Dual Chain Output------")
print(dual_chain_result)
print("*"*100)
 