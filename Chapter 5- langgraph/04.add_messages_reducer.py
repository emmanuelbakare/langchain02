# using reducer and Message and llm

# adding a reducer to a TypedDict for messages and other values
from typing import TypedDict,List, Annotated
from langgraph.graph import StateGraph, START,END

#reducers
from langgraph.graph.message import add_messages # used to add Messages
from operator import add #used to add list

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

#custom reducer
def add_nums(current, new):
    return current + new

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    animals: Annotated[List[str],add]
    count: Annotated[int, add_nums]

#declare chat nodes
def chat_node(state:AgentState):
    conversation_history = state["messages"]  #store the dict messages value into conversation_history
    response = llm.invoke(conversation_history) #do an LLM call of the content of conversation_history
    return { # this returns an AImessage and it is added to the already existing message (conversation_history message)
        "messages": response 
    }
 
graph = StateGraph(AgentState)

graph.add_node("chat_node",chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node",END)

agent = graph.compile()

message1 = HumanMessage(content = "Hello my name is Emmanuel")

turn1_state = agent.invoke({
    "messages":message1
})

print("--- Graph After First Run------")
print(turn1_state)
print("*"*30)

#Turn 2
message2 = HumanMessage(content = "What is your favourite color")

turn2_state = agent.invoke({
    "messages": turn1_state["messages"] + [message2] # merge the initial conversation with the new message2 conversation.
    # "messages": message2 # if you dont merge the messages as above, you will only get a last conversation message2  (HumanMEssage and it AIMessage) in the output
})

print("--- Graph After Second Run------")
print(turn2_state)
print("*"*30)

