#using different anthropic models
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()

# llm = ChatAnthropic(model="claude-sonnet-4-6") #Coding & Daily Use : Faster and smarter than 3.5 Sonnet; excellent at complex logic and tool use.
# llm = ChatAnthropic(model="claude-opus-4-6") #Complex Reasoning: " Best for legal analysis, high-level strategy, and multi-step scientific research.
llm = ChatAnthropic(model="claude-haiku-4-5") #Speed & Volume : Extremely cheap and near-instant; perfect for simple classification or data extraction.

System = SystemMessage(content = "output only the answer and do not add any prefix or suffix description")
messages = [
    SystemMessage(content = "output only the answer and do not add any prefix or suffix description"),
    HumanMessage(content = "write a very short poem about prayer to Jesus")
] 

result = llm.invoke(messages)
content = result.content
print(content)