from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

class GraphState(TypedDict):
    input:str
    results: str 

class ContextSchema(TypedDict):
    user_id : str 

def plain_node(state: GraphState):
    print("Executing 'plain_node'...")
    return {"results": f"Hello {state['input']}"}

def node_with_config(state:GraphState, config:RunnableConfig):
    print("Executing 'node_with_config...")

    thread_id = config.get("configurable",{}).get("thread_id")

    print(f"----Accessed thread_id from config: {thread_id}")

    return {"results":"Config Succesfully Accessed"}

def node_with_runtime(state:GraphState, runtime: Runtime[ContextSchema]):
    print("Executing 'node_with_runtime'...")

    user_id = runtime.context['user_id']

    print(f"----Accessed user_id from the runtime: {user_id}")

    return state

builder = StateGraph(GraphState, context_schema=ContextSchema)

builder.add_node("plain_node", plain_node)
builder.add_node("node_with_config", node_with_config)
builder.add_node("node_with_runtime", node_with_runtime)

builder.add_edge(START, "plain_node")
builder.add_edge("plain_node", "node_with_config")
builder.add_edge("node_with_config","node_with_runtime")

graph = builder.compile()

#run the graph
initial_state = {
    'input': "Emmanuel Bakare"
}

run_config = {
    "configurable":{
        "thread_id": "029111"
    }
}

graph_context = {
    "user_id": "user-001"
}

final_state = graph.invoke (
    input = initial_state,
    config = run_config,
    context= graph_context
)

print("Final State:")
print(final_state)