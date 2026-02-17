"""
Task: Content generation pipeline with quality control

Description: get a topic and how you want it generated, after generating an initial draft, pass it through another llm to
verify the authenticity and facts of the draft, them improve, then format it into a publication using the improvement. 
This uses different llm call for this actions

Input:
- Topic
- Quality requirements

Steps:
- Generate an initial draft
- Fact check the draft
- Improve the draft based on recommendation from the previous step
- Format for publication
"""


from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

class ContentState(TypedDict):
    topic: str
    requirements: str
    draft: str
    fact_check_results: str 
    improved_content: str 
    final_draft: str  

llm = ChatOpenAI(model = "gpt-4o")

# DEFINE NODES

#STEP 1

def generate_draft(state: ContentState) ->ContentState:
    """Gnerate initial blog post draft"""

    prompt = f"""
        Write a 200-word blog post about: {state['topic']}
        requirements: {state['requirements']}
        Focus on creating engaging, informative content
    """
    
    draft = llm.invoke(prompt).content

    print("==== Step 1: Draft Generated =======")
    print(draft[:150] + "...\n")

    return {
        "draft": draft
    }


#STEP 2:

def fact_check(state:ContentState)->ContentState:
    """ Check draft for factual accuracy and consistency"""

    prompt=f"""
    Review the following blog post draft for factual accuracy and consistency:

    {state['draft']}

    Identify:
    1. Any factual claims that seem questionable
    2. Internal Inconsistencies
    3. Statements that need citations

    provide a brief report.
     """
    
    fact_check_results =llm.invoke(prompt).content

    print("==== Step 2: Fact Check Complete =======")
    print(fact_check_results[:150] + "...\n")

    return {
        "fact_check_results": fact_check_results
    }

def  improve_content(state:ContentState)->ContentState:
    """ Revise content based on fact check feedback"""

    prompt =f"""
    Here is a blog post draft:
    {state['draft']}

    Here is a feedback from fact-checking the draft:
    {state['fact_check_results']}

    Revise the blog post to address the feeback while maintaining engaging writing. Keep it around 200 words
    """
    improved = llm.invoke(prompt).content

    print("==== Step 3: Content Improved =======")
    print(improved[:150] + "...\n")

    return {
        "improved_content": improved
    }

#STEP 4 Formart wha we have generated
def format_output(state:ContentState)->ContentState:
    """ Format content with HTML tags and elements"""

    prompt = f"""
    Format the following blog post for web publication:
    {state['improved_content']}

    Add:
    - An engaging title wrapped in <h1> tags
    - Subheadings where appropriate with <h2> tags
    - Paragraph tags <p>
    - A meta description (1-2 sentences)

    output the formatted HTML.
    """

    final = llm.invoke(prompt).content

    print("==== Step 4: Formatted for Publication =======")
    print(final[:200] + "...\n")

    return {
        "final_draft": final
    }


builder = StateGraph(ContentState)

builder.add_node(generate_draft)
builder.add_node(fact_check)
builder.add_node(improve_content)
builder.add_node(format_output)

builder.add_edge(START,"generate_draft")
builder.add_edge("generate_draft","fact_check")
builder.add_edge("fact_check","improve_content")
builder.add_edge("improve_content","format_output")
builder.add_edge("format_output", END)

graph = builder.compile()

result = graph.invoke({
    "topic": "The benefit of morning exercise",
    "requirements": " Target audeince: busy professionals. Inlcude practicals"
})

print("\n"+ "*"*50)
print("===FINAL RESULT===")
print("*"*50)
print(result['final_draft'])


    
    

    