# simple langgraph with 2 nodes
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages

#define  our State

class SimpleState(TypedDict):
    messages: Annotated[List, add_messages]

graph = StateGraph(SimpleState)

#2. Create nodes
def say_hello(state:SimpleState):
    print("Executing 'say hello' mode ")
    return {
        "messages":["hello"]
    }

def say_world(state:SimpleState):
    print("Executing 'say world' node...")
    return {
        "messages":["world"]
    }

graph.add_node("say_hello",say_hello)
graph.add_node("say_world",say_world)

#3.  link node with edges
#START ->say_hello ->say_world-> END

graph.add_edge(START, "say_hello")
graph.add_edge("say_hello","say_world")
graph.add_edge("say_world",END)

#4. Compile graph
agent = graph.compile() #returns runnable

#5. Run Graph
initial_state = {
    "messages":[]
}

final_state = agent.invoke(initial_state)


#a graphical ASCII representation
print(agent.get_graph().draw_ascii())

print("\n----FINAL STATE-----")
print(final_state)