from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv
from typing import TypedDict

"""actions to take
1. Create the type dictionary  TypeDict (ContentState) for storing the data
2. create all the functions that will generate the content and pass the result into the TypedDict
    a. generate_draft - create the first draft of the document (this will take in topic and requirement)
    b. fact_check - Fact check the content created in a above - this takes in the draft created in a
    c. improved_draft -  this uses the draft in a and the suggestion in b to create a new improved draft 
    d.  format_output - the new improved draft is then formated in certain way
 """

load_dotenv()

class ContentState(TypedDict):
    topic: str
    requirements: str 
    draft: str 
    fact_check_result: str 
    improved_content: str 
    final_draft: str 

llm = ChatOpenAI(model="gpt-4o-mini")

def generate_draft(state:ContentState)->ContentState:

    prompt = f"""
    Write a 200 word blog post about: {state['topic']}
    requirements: {state['requirements']}
    Focus on creating an engaging and informative content
"""
    result = llm.invoke(prompt).content

    print("==============Step 1: Draft==============")
    print(result[:150]+ '....\n\n')

    return {
        "draft":result
    }

#based on the draft created in generate_draft review and give suggestions for improvement
def fact_check(state:ContentState)->ContentState:
    prompt = f""" 
Review the following blog post draft for factual accuracy and consistency:

    {state['draft']}

    Identify:
    1. Any factual claims that seem questionable
    2. Internal Inconsistencies
    3. Statements that need citations

    provide a brief report.
"""
    result= llm.invoke(prompt).content

    print("==== Step 2: Fact Check Complete =======")
    print(result[:150] + "...\n")
    
    return {
        "fact_check_result":result
    }



# based on suggested improvements, generate an improved version on the draft
def  improved_draft(state:ContentState)->ContentState:
    prompt = f"""
    Here is a blog post draft:
        {state['draft']}
    
        Here is a feedback from fact-checking the draft:
        {state['fact_check_result']}
    
        Revise the blog post to address the feeback while maintaining engaging writing. Keep it around 200 words
 """
    result = llm.invoke(prompt).content

    print("==== Step 3: Content Improved =======")
    print(result[:150] + "...\n")
    return {
        "improved_content":result
    }

# Format the improved content into a proper, fine tuned content.
def  format_output(state:ContentState)->ContentState:

    prompt = f"""
    Format the following blog post for web publication:
    {state['improved_content']}

    Add:
    - An engaging title wrapped in <h1> tags
    - Subheadings where appropriate with <h2> tags
    - Paragraph tags <p>
    - A meta description (1-2 sentences)

    output the formatted HTML. """

    result = llm.invoke(prompt).content

    print("==== Step 4: Formatted for Publication =======")
    print(result[:200] + "...\n")
    
    return {
        "final_draft":result
    }

builder = StateGraph(ContentState)

builder.add_node(generate_draft)
builder.add_node(fact_check)
builder.add_node(improved_draft)
builder.add_node(format_output)

builder.add_edge(START, "generate_draft")
builder.add_edge("generate_draft","fact_check")
builder.add_edge("fact_check", "improved_draft")
builder.add_edge("improved_draft","format_output")
builder.add_edge("format_output", END)

graph = builder.compile()

final_output = graph.invoke({
    "topic":"Benefit of Artificial Intelligence",
    "requirements":"Target Audience: IT Professionals and Content Creators"
})

print("="*50)
print("="*50)
print(final_output['final_draft'])
print("="*50)
print("="*50)