from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()
prompt1= PromptTemplate(template="Who is the president of Nigeria")

prompt2 = PromptTemplate.from_template("who is the president of Togo")
prompt3 = PromptTemplate.from_template("who is the president of {country}")

# print(prompt1.invoke({}))  # print a prompt value
# print(prompt2.format())

# print(prompt3.invoke({"country":"France"}))

llm = ChatOpenAI(model="gpt-4o")

response = llm.invoke(prompt2.format())
print(response.content)

