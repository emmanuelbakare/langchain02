# adding a reducer to a TypedDict for messages and other values
from typing import TypedDict,List, Annotated
from langgraph.graph import StateGraph, START,END

#reducers
from langgraph.graph.message import add_messages # used to add Messages
from operator import add #used to add list

from langchain_core.messages import BaseMessage, HumanMessage

#custom reducer
def add_nums(current, new):
    return current + new

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    animals: Annotated[List[str],add]
    count: Annotated[int, add_nums]

#declare two nodes
def node_a(state:AgentState):
    print("RUNNING NODE A")
    return {
        "messages":[HumanMessage(content="Coming from Node A")],
        "animals": ["Bird"],
        "count":1
    }
def node_b(state:AgentState):
    print("RUNNING NODE B")
    return {
        "messages":[HumanMessage(content="Coming from Node B")],
        "animals": ["Lion"],
        "count":10
    }

graph = StateGraph(AgentState)

#add nodes
graph.add_node("node_a",node_a)
graph.add_node("node_b",node_b)

#add Edges
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", END)

agent = graph.compile()

initial_state = {
    "messages":[HumanMessage(content="Start Here")],
    "animals" :[],
    "count": 0
}

final_state = agent.invoke(initial_state)



print("*"*50)
print("---------ASCII DIAGRAM--------")
print(agent.get_graph().draw_ascii())


print("*"*50)
print(final_state)