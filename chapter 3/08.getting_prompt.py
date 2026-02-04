from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv


load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template("Write a short, concise sentence about {topic}")

simple_chain = prompt | model | StrOutputParser()

fact_checking_prompt = ChatPromptTemplate.from_messages([
    ("system","Start by quoting the statement, then give the reason"),
    ("user","How correct is this statement: {statement}")
])

checker_chain = fact_checking_prompt | model | StrOutputParser()

fact_checking_chain = {"statement":simple_chain} | checker_chain

all_prompts = fact_checking_chain.get_prompts()

for i, prompt in enumerate(all_prompts):
    print(f"____Prompt {i + 1}---------")
    print(prompt.pretty_repr())
    print("*"*70)