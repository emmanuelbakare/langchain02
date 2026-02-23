from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()


llm = ChatAnthropic(model="claude-haiku-4-5")

System = SystemMessage(content = "output only the answer and do not add any prefix or suffix description")
messages = [
    SystemMessage(content = "output only the answer and do not add any prefix or suffix description"),
] 

while True:
    user_prompt = input("Question>> ")

    if user_prompt.lower() in ("exit","quit"):
        break

    messages.append(HumanMessage(content = user_prompt))
    result = llm.invoke(messages)
    content = result.content
    print(content)