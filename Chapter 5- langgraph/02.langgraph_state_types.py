
from langgraph.graph import StateGraph,START, END
#more typedict imports
from typing import Annotated, TypedDict,List 
from langgraph.graph.message import add_messages

#for pydantic imports
from pydantic import BaseModel, Field 
from langchain_core.messages import BaseMessage

def node_a(state):
    """ A simple node that update the state"""
    print("Executing Node A....")
    return {
        "messages":["Step A Completed"],
        "step_count": 1
    }

def node_b(state):
    """ A simple node that update the state"""
    print("Executing Node B....")

    if isinstance(state,dict):
        step_count = state["step_count"]
    else:
        step_count = state.step_count

    print("Current step count from state: {step_count}")

    return {
        "messages":["Step B Completed"],
        "step_count": 1
    }

def build_and_run_graph(state_schema, initial_state):
    print(f"\n--- Building and Running graph with state schema: {state_schema.__name__ if hasattr(state_schema,'__name__') else 'Dictionary'}")

    #initiate the graph
    graph = StateGraph(state_schema)

    #add Node
    graph.add_node("node_a",node_a)
    graph.add_node("node_b",node_b)

    #add Edges
    graph.add_edge(START,"node_a")
    graph.add_edge("node_a","node_b")
    graph.add_edge("node_b",END)

    agent = graph.compile()

    final_state = agent.invoke(initial_state)

    print("\nFinal State:")
    print(final_state)
    print("*"*40)


#01. Using a Plain Dictionary as the schema

# def create_dict_state():
#     return{
#         "messages":[],
#         "step_count":0,
#         "private_data":None
#     }

# build_and_run_graph(dict, create_dict_state())


#02. Using TypedDict

def custom_add(current:int, new:int)-> int:
    return current + new

# class TypedDictState(TypedDict):
#     messages: Annotated[List[str], add_messages]
#     step_count : Annotated[int,custom_add]

# build_and_run_graph(TypedDictState, {
#     "messages":[],
#     "step_count": 0,
#     "private_data": ""
# })



#03. Using Pydantic as schema

class PydanticState(BaseModel):
    messages: Annotated[List[BaseModel], add_messages] = Field(default_factory=list)
    step_count: Annotated[int, custom_add] = Field(default=0)
    private_data: str = Field(default="")

build_and_run_graph(PydanticState, PydanticState())
