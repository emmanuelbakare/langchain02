from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
message="give me a one paragraph sentence of where do I find crab the most?"
prompt1 = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a geologist."),
    HumanMessage(content=message)
])

prompt2= PromptTemplate.from_template(message)
prompt3= ChatPromptTemplate.from_template(message)
 
# response  = llm.invoke({'input':'what is your name'})
lines = '='*30
print(f"{lines} PROMPT1: ChatPromptTemplate.from_messages{lines}")
print(prompt1)
print(f"{lines} PROMPT2: PromptTemplate.from_template OUTPUT {lines}")
print(prompt2)
print(f"{lines} PROMPT3: ChatPromptTemplate.from_template OUTPUT {lines}")
print(prompt3)
prompt4 =[
    ('system','You are a scientist'),
    ('user',message)
]


prompt5 = [
    {'system':'you are a scientist'},
    {'user':message}
]

prompt6 = [
    SystemMessage(content= "You are a scientist"),
    HumanMessage(content=message)
]


print()
print()

print(f"{lines} MESSAGES OUTPUT {lines}")
print(f"{lines} PROMPT 3: ChatPromptTemplate.from_messages format_messages {lines}")
print(prompt1.format_messages())
print(f"{lines} PROMPT 2:  PromptTemplate.from_template.format_prompt() {lines}")
print(prompt2.format_prompt())
print(f"{lines} PROMPT 3:  ChatPromptTemplate.from_template.format_prompt() {lines}")
print(prompt3.format_prompt())
print(f"{lines} PROMPT 5: List of tuple OUTPUT {lines}")
print(prompt4)
print(f"{lines} PROMPT 5: List of dictionary OUTPUT {lines}")
print(prompt5)
print(f"{lines} PROMPT 5: List of SystemMessage, HumanMessage OUTPUT {lines}")
print(prompt6)

# response = llm.invoke(prompt)
print()
print()
#output options with different input above
print(f"{lines} LLM OUTPUT {lines}")
# response = llm.invoke(prompt1.format_messages()) # convert message to a list of messages [ SystemMessage, HumanMessage] 
# response = llm.invoke(prompt2.format_prompt())
# response = llm.invoke(prompt2.format_prompt())

response =llm.invoke(prompt6)
print(response.content)

"""
Output:

============================== PROMPT1: ChatPromptTemplate.from_messages==============================
input_variables=[] input_types={} partial_variables={} messages=[SystemMessage(content='You are a geologist.', additional_kwargs={}, response_metadata={}), HumanMessage(content='give me a one paragraph sentence of where do I find crab the most?', additional_kwargs={}, response_metadata={})]
============================== PROMPT2: PromptTemplate.from_template OUTPUT ==============================
input_variables=[] input_types={} partial_variables={} template='give me a one paragraph sentence of where do I find crab the most?'
============================== PROMPT3: ChatPromptTemplate.from_template OUTPUT ==============================
input_variables=[] input_types={} partial_variables={} messages=[HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='give me a one paragraph sentence of where do I find crab the most?'), additional_kwargs={})]


============================== MESSAGES OUTPUT ==============================
============================== PROMPT 3: ChatPromptTemplate.from_messages format_messages ==============================
[SystemMessage(content='You are a geologist.', additional_kwargs={}, response_metadata={}), HumanMessage(content='give me a one paragraph sentence of where do I find crab the most?', additional_kwargs={}, response_metadata={})]
============================== PROMPT 2:  PromptTemplate.from_template.format_prompt() ==============================
text='give me a one paragraph sentence of where do I find crab the most?'
============================== PROMPT 3:  ChatPromptTemplate.from_template.format_prompt() ==============================
messages=[HumanMessage(content='give me a one paragraph sentence of where do I find crab the most?', additional_kwargs={}, response_metadata={})]
============================== PROMPT 5: List of tuple OUTPUT ==============================
[('system', 'You are a scientist'), ('user', 'give me a one paragraph sentence of where do I find crab the most?')]
============================== PROMPT 5: List of dictionary OUTPUT ==============================
[{'system': 'you are a scientist'}, {'user': 'give me a one paragraph sentence of where do I find crab the most?'}]
============================== PROMPT 5: List of SystemMessage, HumanMessage OUTPUT ==============================
[SystemMessage(content='You are a scientist', additional_kwargs={}, response_metadata={}), HumanMessage(content='give me a one paragraph sentence of where do I find crab the most?', additional_kwargs={}, response_metadata={})]


============================== LLM OUTPUT ==============================
You can find crabs most abundantly in coastal areas and estuaries, particularly in rocky tidal pools, sandy beaches, and mangroves, as these habitats provide the ideal conditions for various crab species to thrive, with abundant food sources, shelter from predators, and access to both saltwater and freshwater environments.

"""