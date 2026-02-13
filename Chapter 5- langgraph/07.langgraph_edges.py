from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class GraphState(TypedDict):
    input: str
    execution_path: list[str]

def node_a(state:GraphState)->dict:
    print("Executing 'node_a'...")

    new_path = state.get("execution_path",[])+ ["node_a"]

    return {
        "execution_path": new_path
    }

def node_b(state:GraphState)->dict:
    print("Executing 'node_b'...")

    new_path = state.get("execution_path",[])+ ["node_b"]

    return {
        "execution_path": new_path
    }

def node_c(state:GraphState)->dict:
    print("Executing 'node_c'...")

    new_path = state.get("execution_path",[])+ ["node_c"]

    return {
        "execution_path": new_path
    }

def node_d(state:GraphState)->dict:
    print("Executing 'node_d'...")

    new_path = state.get("execution_path",[])+ ["node_d"]

    return {
        "execution_path": new_path
    }

#write a conditional edge
def should_continue(state:GraphState):
    print("Evaluating conditional edge")
    if "go_to_c" in state['input']:
        print("----> Continuing to C")
        return "node_c"
    else:
        print("---> continuing to D")
        return "node_d"
    
builder = StateGraph(GraphState)

builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
builder.add_node(node_d)

builder.add_edge(START, "node_a")
builder.add_edge("node_a","node_b")
builder.add_conditional_edges("node_b", should_continue)
builder.add_edge("node_c", END)
builder.add_edge("node_d", END)

graph = builder.compile() 

initial_state_1 = {
    'input': "Hello Langraph is awesome"
}

final_state_1 = graph.invoke(initial_state_1)

print("---------Final State 2:-------------------")
print(final_state_1)

#
initial_state_2 = {
    'input': "Hello Langraph is awesome go_to_c"
}

final_state_2 = graph.invoke(initial_state_2)

print("Final State 2:")
print(final_state_2)

