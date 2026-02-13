from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage



# declare the state class. you can use class MyGraphState(MessagesState) or 
# class MyGraphState(TypedDict) if you use the class with TypedDict, you will have to define the messages parameter
# if you use the one with MessagesState you dont need to define the messages parameter because it already comes with it
# the example below as two parameter turn_count and messages. messages parameter was not defined because we use MessagesState.
class MyGraphState(MessagesState):
    turn_count: int 

def user_node(state:MyGraphState)->dict:
    print("Executing 'use_node'")

    return {
        "messages": HumanMessage(content="What is the weather like today")

    }

def ai_node(state:MyGraphState):
    print("Executing 'ai_node'")

    last_message = state['messages'][-1].content
    print(f'Human Prompt {last_message}')

    response_content = f"I have received you last message '{last_message}' and I am with it"

    return {
        "messages":AIMessage(content=response_content)
    }

def counter_node(state: MyGraphState):
    print("Executing a'counter_node....")

    return {
        "turn_count": state["turn_count"] + 1
    }

graph = StateGraph(MyGraphState)

graph.add_node( user_node)
graph.add_node( ai_node)
graph.add_node( counter_node)

graph.add_edge(START,"user_node")
graph.add_edge("user_node","ai_node")
graph.add_edge("ai_node","counter_node")
graph.add_edge("counter_node", END)

agent = graph.compile()

initial_state = {
    "turn_count": 0 
}

final_state = agent.invoke(initial_state)

print("---final state-----")
print(final_state)