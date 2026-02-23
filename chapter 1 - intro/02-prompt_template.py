from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()
prompt1= PromptTemplate(template="Who is the president of Nigeria")

prompt2 = PromptTemplate.from_template("who is the president of Togo")
prompt3 = PromptTemplate.from_template("who is the president of {country}")

# print(prompt1.invoke({}))  # print a prompt value. outputs "text='Who is the president of Nigeria'"
# print(prompt2.format()) # outputs "who is the president of Togo"

# print(prompt3.invoke({"country":"France"})) # outputs "text='who is the president of France'"

llm = ChatOpenAI(model="gpt-4o")

response = llm.invoke(prompt2.format())
print(response.content)
"""
Outputs:
As of my last update, the President of Togo is Faure Gnassingbé. He has been in office since May 2005, following the death of his father, Gnassingbé Eyadéma, who had been president since 1967. Please verify with up-to-date sources, as there may have been changes or updates since then.
"""
