from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model='gpt-4o')



# prompt = ChatPromptTemplate([
#     ('system','reply every prompt in Yoruba language'),
#     ('user','Who is the president of Nigeria')
# ])

#print(prompt.format())
# response = llm.invoke(prompt.format())
# print(response.content)


prompt = ChatPromptTemplate([
    ('system','reply every prompt in {language} language'),
    ('user','Who is the president of {country}')
])

myPrompt = prompt.invoke({
    "language":"English",
    "country":"Nigeria"
})
response = llm.invoke(myPrompt)

print(response.content)