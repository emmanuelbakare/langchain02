#This code create different topics and then use SEND to processes a more details information about each title in parallel form using SEND

from typing import TypedDict, Annotated, List 
from operator import add 
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

# define a main topic, break it down into subtopics, then research each subtopics into research_subtopics
class OverallState(TypedDict):
    topic: str
    subtopics: List[str]
    research_results: Annotated[List[str], add]
    final_report: str

#this state operates in each SEND operation
class ResearchState(TypedDict):
    subtopic: str 
    research_results: List[str]

#### GENERATE NODES

#this node generate our first subtopics
def generate_subtopics(state:OverallState):
    topic = state['topic']

    #-- generate the sub topics
    #--- use an llm to generate this , or from a database
    subtopics = [
        f"{topic} - History",
        f"{topic} - Current Trend",
        f"{topic} -  Future Outlook",
    ]

    return {
        'subtopics': subtopics
    }


#this node will generate each subtopic details
def research_subtopics(state:ResearchState):
    subtopics = state['subtopic']

    # you can get the result from an llm or api
    result = f"Research Finding on {subtopics}: [Detailed analysis, data, insidts]"

    return {
        'research_results': [result]
    }

def combile_report(state:OverallState):
    results = state['research_results']
    report  = "=" * 50 + "\n"
    report += "COMPREHESIVE RESEARCH REPORT \n"
    report  += "=" * 50 + "\n"

    for i, result in enumerate(results,1):
        report +=f" {i}. {result}\n\n"

    return {
        "final_report": report
    }
    

def continue_to_research(state:OverallState):

    return [
        Send("research_subtopics", {"subtopic":s}) 
        for s in state['subtopics']
    ]

builder = StateGraph(OverallState)

builder.add_node(generate_subtopics)
builder.add_node(research_subtopics)
builder.add_node(combile_report)

builder.add_edge(START, "generate_subtopics")
builder.add_conditional_edges("generate_subtopics", continue_to_research)
builder.add_edge("research_subtopics","combile_report")
builder.add_edge("combile_report", END)

graph = builder.compile()

initial_state = {
    "topic": "Artificial Intelligence",
    "subtopics":[],
    "research_results": [],
    "final_report": ""
}

final_state = graph.invoke(initial_state)

print("-----FINAL STATE----")
print(final_state['final_report'])