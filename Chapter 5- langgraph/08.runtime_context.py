#Use Runtime Context when you want to pass static, per-run dependencies / configuration values that many parts of the graph
#  need to read, but should not live in (and should not pollute) the agent's mutable working memory (state).
from dataclasses import dataclass
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

class GraphState(TypedDict):
    input: str
    result: str 

#we used dataclass so that we can have defalt values in the declaration. 
# Use TypedDict if you dont need default values at the defination level - ony capture state
@dataclass
class MyGraphContext:
    user_agent: str   # a default value not set in the context here must be defined in the invoke under context field
    docs_url: str = "https://docs.langchain.com"
    db_connection: str = "mysql://user:password@localhost:3306/my_db"

def context_access_node(state:GraphState, runtime: Runtime):
    print("Executing node context_access_node")
    db_string = runtime.context.db_connection
    docs_url = runtime.context.docs_url 
    user_agent = runtime.context.user_agent 

    print("Current DB String", db_string)
    print("Documentation URL:", docs_url)
    print("User Agent:", user_agent)

    return {
        "result": f"Content Accessed. DB: {db_string.split('//')[0]}..."
    }


builder = StateGraph(GraphState, context_schema=MyGraphContext)

builder.add_node(context_access_node)

builder.add_edge(START, "context_access_node")
builder.add_edge("context_access_node", END)

graph = builder.compile()

initial_state =  {'input': "Start Process"}

final_state = graph.invoke(
    initial_state,
    context= {
        "user_agent": "Default_Platform", # user_agent must be defined because it has no default value in the context class defination
       # you can override any initially defined value
        "db_connection": "postgres://new_user@remote_host:5432/production" 
        }) 

print("Final State")
print(final_state)
