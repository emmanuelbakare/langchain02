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
print(myPrompt,"\n", type(myPrompt))
"""
outputs:
messages=[SystemMessage(content='reply every prompt in English language', additional_kwargs={}, response_metadata={}), HumanMessage(content='Who is the president of Nigeria', additional_kwargs={}, response_metadata={})] 
 <class 'langchain_core.prompt_values.ChatPromptValue'>
"""
# response = llm.invoke(myPrompt)

# print(response.content)