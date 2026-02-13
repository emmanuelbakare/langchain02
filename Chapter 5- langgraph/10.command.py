from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class GraphState(TypedDict):
    temperature: int 
    status_message: str 
    warning_sent: bool 
    final_action_performance: str 


def  check_temp_node(state:GraphState)-> Command[Literal["warn_user", "success"]]:
    temp =  state ['temperature']

    if temp > 90:
        print('---- ALERT: Temp too high! Usssuing command to warn user----')

        return Command(
            update = {
                "status_message": "Routing to warning handler ....",
            },
            goto = "warn_user"
        )
    else:
        print("----OK: Temp is OK, Issuing Command to 'success'-----")

        return Command(
            update= {
                "status_message": "Rounting to Success Handler....",
            },
            goto = "success"
        )
    
def warn_user(state:GraphState):
    print(f"Executing warn_user: Warning successfully sent at  {state['temperature']}")

    return {
        "warning_sent": True,
        "final_action_performed": "Warning notification sent"
    }
    
def success(state:GraphState):
    print(f"Executing success_user:All System clear")

    return {
        "final_action_performed": "Temperator Safety Confirmed @ {state['temperature']} temp"
    }
                                                
builder = StateGraph(GraphState)

builder.add_node(check_temp_node)                                           
builder.add_node(warn_user)                                           
builder.add_node(success)    

builder.add_edge(START, "check_temp_node")

graph= builder.compile()
### TEst the Graph###

initial_state = {
    "temperature":40
}

final_state = graph.invoke(initial_state)

print("---FINAL STATE ----")
print(final_state)