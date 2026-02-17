# Use parallelization to process information through different llm at same time
# you can use it to send a post to different social media at the same time
#ensuring that each social media post is created according to the social media specification
#this make differnt call to the llm but at same time

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class OverallState(TypedDict):
    topic: str
    instagram_post: str
    twitter_post: str
    linkedin_post: str
    final_output: str 

llm = ChatOpenAI(model="gpt-4o-mini")

def generate_instagram(state: OverallState)->OverallState:
    """ Generate an engaging  Instagram post with emojis and hastags"""

    prompt = f"""
    Create an Instagram post about: {state['topic']}

    Requirements:
    - Engaging and visual language
    - 2 to 3 short paragraph (150 -200 words max)
    - Include relevenat emojis
    - End with 5-8 relevant hashtags
    - Casual, firendly tone
    - Call-to-action to engage with the post

    Make it perfect for Instagram's audience
    """
    instagram_post = llm.invoke(prompt).content 
    
    print("Instagram Generator: Complete")

    return {
        "instagram_post": instagram_post
    }

def generate_twitter(state: OverallState)->OverallState:
    """ Generate a concise twitter post"""

    prompt = f"""
    Create a twitter  post about: {state['topic']}

    Requirements:
    - Maximum  280 characters (this is crucial)
    - Punchy and attention=grabbing
    - Including 2-3 relevant hashtags
    - Conversational tone
    - Can use emojis sparingly
    - Should spark engagement/replies

    Make it perfect for Twitter's fast-paced environment.
    """
    twitter_post = llm.invoke(prompt).content 
    
    print("Twitter Generator: Complete\n")

    return {
        "twitter_post": twitter_post
    }

def generate_linkedin(state: OverallState)->OverallState:
    """ Generate a professional LinkedIn post"""

    print(" LinkedIN GEnerator: Creating post...")

    prompt = f"""
    Create a LinkedIn  post about: {state['topic']}

    Requirements:
    - Professinoal yet engagin tone
    - 3-4 paragraphs (200-300 words)
    - Inlcude insights or lessions learned
    - Use line breaks for readability
    - Add 3-5 professional hashtags
    - Inlcude a though-provoking questioin at the end
    - Focus on value and professional development
    """
    linkedin_post = llm.invoke(prompt).content 
    
    print("LinkedIn Generator: Complete\n")

    return {
        "linkedin_post": linkedin_post
    }

#aggregator node 
def aggregate_post(state:OverallState)-> OverallState:
    """Combine all platfomrs posts into a formatted final output"""
    
    print(" Aggregator: Combinining all posts....")
    final_output = f"""
    {'='*70}
    SOCIAL MEDIA CONTENT PACKAGE
    {'='*70}
    
    Topic: {state['topic']}

    {'='*70}
    INSTAGRAM
    {'='*70}
    {state['instagram_post']}

    {'='*70}
    TWITTER
    {'='*70}
    {state['twitter_post']}

    {'='*70}
    LINKEDIN
    {'='*70}
    {state['linkedin_post']}

    """

    return {
        "final_output":final_output
    }


# create a paralle workflow - start by creating graph
builder = StateGraph(OverallState)

builder.add_node(generate_instagram)
builder.add_node(generate_twitter)
builder.add_node(generate_linkedin)
builder.add_node(aggregate_post)

builder.add_edge(START, "generate_instagram")
builder.add_edge(START, "generate_twitter")
builder.add_edge(START, "generate_linkedin")

builder.add_edge("generate_instagram", "aggregate_post")
builder.add_edge("generate_twitter", "aggregate_post")
builder.add_edge("generate_linkedin", "aggregate_post")

builder.add_edge("aggregate_post", END)

graph = builder.compile()

topic = "The Impact of AI on workplace productivity"

print("\n TOPIC: {topic}")

result = graph.invoke({
    "topic": topic,
    "instagram_post": "",
    "twitter_post": "",
    "linkedin_post": "",
    "final_output": ""
})

print("====FINAL OUTPUT=====")
print(result.get("final_output", "NO SOCIAL MEDIA OUTPUT FOUND"))






