from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from typing import TypedDict, List, Annotated
from operator import add
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from work_tool import write_to_file # custom function to copy output to file

load_dotenv()

#define the overall state that will be for the entire grapy
class OverallState(TypedDict):
    research_topic: str
    sources: List[str]
    worker_findings: Annotated[List[dict], add]
    final_report:  str 

# private state that each worker will operate with
class WorkerState(TypedDict):
    source: str
    worker_id: int 
    research_topic: str 

# create the output of the orchestrator. The orchestrator needs to produced a structured output.
class ResearchPlan(BaseModel):
    sources: List[str] = Field(
        description="List of specific research sources/aspect to investigate",
        max_length=5
    )
    reasoning: str = Field( # make the llm tell us why the sources are chosen
        description="Brief explanation of why these sources where chosen"
    )     

llm = ChatOpenAI(model="gpt-4o")

# create 3 nodes 1.
# Node 01: Orchestrator Node -  this takes our topic and slice it into different sources/topic
# Node 02 : Worker Node -  instance of the worker node. works on each topic/sources generated from the orchestrator node
# Node 03 : Synthesizer node -  brings together all the finds from the worker nodes and prepare a final report from it.

# Node 1:  Orchestrator Node:
def plan_research(state:OverallState) ->OverallState:
    print("\n"+ "="*70)
    print("ORCHESTRATOR: Planning research Strategy")
    print("="*70)
    print(f"Topic: {state['research_topic']}\n")

    planner_llm = llm.with_structured_output(ResearchPlan)

    prompt = f"""
        You are a research strategiest planning a comprehensive investigation

        Research Topic: {state['research_topic']}

    CRITICAL INSTRUCTION: Generate between 3-5 specific research sources or aspects to investigate.
    DO NOT generate more than 5 sources.

    Each Source should be:
    - Specific and focused on a distinct aspect
    - Relevant to the overall topic
    - Complementary to other sources (minimal overlap)
    - Concrete enough to guide targeted research

    Examples of good sources:
    - "Clinical trial results and efficacy data"
    - "Economic impact and const-benefits analysis"
    - "Regulatory framework and compliance requirements"
    - "Patient outcomes and quality of life metrics"
    - "Industry adoption rates and market trends"

    Generate sources that will provide comrehensive coverage fo the topic
    """

    research_plan = planner_llm.invoke(prompt)

    print(f" Orchestrator Generated: {len(research_plan.sources)}")

    for i, source in enumerate(research_plan.sources, 1):
        print(f"{i}. {source}")

    print(f"\n Reasoning: {research_plan.reasoning}")
    print("Preparing to dispatch to nodes...")

    return {
        "sources": research_plan.sources
    }

#Node 2:  Worker Node
# this takes in a private state and returns it result back to the overallstate
# it recieves data in the private WorkerState and return the final result to Overallstate
def research_worker(state:WorkerState) -> OverallState:
    worker_id = state["worker_id"]
    source = state["source"]

    print(f" WORKER ID: {worker_id}: Researching '{source}'...")

    prompt = f"""
    You are a specialized researcher investigating: {state['research_topic']}
    Your specific focus area: {source}

    Conduct thorough reseaerch on this aspect and provide:

    1. KEY FINDINGS (3 -5 specific points)
     - What are the most important discoveries or facts?

    2. DATA & STATISTICS
    - Relevant numbers, percentages, or quantitative information

    3. INSIGHTS & ANALYSIS
    - What does this ifnromation mean?
    - How does it relate to the broader topic?

    4. SOURCES & CREDIBILITY
    - Types of sources you would consult (academic, industry, government, etc)

    5. IMPLICATION
    - Why does this matter for uinderstadning the overall topic?

    Be specific, factual, and provide depth on this particular aspect.
    """
    response = llm.invoke(prompt).content 

    # we are to return a dictionary
    findings ={
        "worker_id": worker_id,
        "source": source,
        "content": response
    }

    print(f"WORKER {worker_id}: Research Complete \n")

    #return back to overallState
    return {
        "worker_findings":[findings]
    }

#NODE 3: Synthesizer 
def synthesize_report(state:OverallState) -> OverallState:
    print("="*70)
    print("SYNTHESIZER: Combining insights from all workers ")
    print("="*70)

    print(f"Processing findings from {len(state['worker_findings'])} research sources")

    all_findings ="\n\n" + "="*70 + "\n\n"
    all_findings += "\n\n".join([
        f"RESEARCH AREA {wf['worker_id']}: {wf['source']}\n {'-'*70}\n {wf['content']}"
        for wf in state['worker_findings']
    ])

    prompt = f""" You are synthesizing a comprehensive research report on : {state['research_topic']}
    You have received detailed findings from {len(state['worker_findings'])} specialized researchers. each investigating a
    different aspect of this topic

    RESEARCH FINDING:
    {all_findings}

    Create a cohesizve, well-structured research report (500-700 words with the following sections:)

    1. EXECUTIVE SUMAARY(2-3 Sentences)
    - Provide a high level overview of the key takeaways

    2. INTRODUCTION
    - Context and improtance of this topic

    3. KEY FINDINGS:
    - Integrate insights from all research areas
    - Organize thematically rather than by source
    - Use specific data and exmaples

    4. ANALYSIS & SYNTHESIS:
    - Identify patterns across different research areas
    - Highlight connections and relationships
    - Note any contradictions or tensions

    5. IMPLICATIONS
    - What do these findings mean
    -Who is affected and how

    6. CONCLUSION
    -  Main takeaways
    - Areas for further research

    IMPORTANT:
    - Write this as a unified, flowing report, NOT as seperate sections from each researcher
    - Integrate finding naturally across themes
    - Use specific examples and data from the research
    - Make it professional and authoritative
    """

    final_report = llm.invoke(prompt).content

    print("SYNTHESIZER: Final Report Complete\n")

    return {
        "final_report": final_report
    }

# now lets take what we get from the worker nodes and dynmaically spin up worker nodes 
#this is done usinng CONDITIONAL EDGE. this spin up SEND command. 
# Each SEND takes piece of the data (source, worker_id) and pass it a worker node

#Conditional Edge Function
def create_research_worker(state:OverallState):
    print("DISPATCHER:  Creating research workers dynamically....")

    # return a list of send command
    # loop through state['sources'] and use each of them to spine up a Send that takes each source (sub-topic), its ID and research_topic
    return [
        Send(
            "research_worker",
            {
                "source": source,
                "worker_id": i + 1,
                "research_topic":  state['research_topic']
            }
        )
        for i , source in enumerate(state['sources'])
    ]

#Build Grapg
builder = StateGraph(OverallState)

builder.add_node("orchestrator", plan_research)
builder.add_node("research_worker", research_worker)
builder.add_node("synthesizer", synthesize_report)

builder.add_edge(START, "orchestrator")
builder.add_conditional_edges(
    "orchestrator",
    create_research_worker,
    ["research_worker"]
)
builder.add_edge("research_worker", "synthesizer")
builder.add_edge("synthesizer", END)

graph = builder.compile()

# give two topics as example. Feedin one at a time 
healthcare_topic = "The impact of artificial Intelligence on healthcare delivery and patient outcomes"
environment_topic = "Renewable energy adoption barriers in developing countries"


topic = environment_topic

print("="*70)
print(f"Topic: {topic}")
print("="*70)

result = graph.invoke ({
    "research_topic":topic,
    "sources":[],
    "worker_findings":[]
})

final_output = result["final_report"]
print("="*70)
print(f"FINAL SYNTHESIZER RESULT")
print("="*70)
print(final_output)

#send output to a file
# with open("final_output.md","w", encoding="utf-8") as f:
#     f.write(final_output)
write_to_file(final_output)



