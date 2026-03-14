from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from typing import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class SocialState(TypedDict):
    topic: str
    instagram_post: str
    twitter_post : str 
    facebook_post : str 
    final_output : str 


#generate instagram post
def generate_instagram(state:SocialState)->SocialState:
    prompt = f"""
    Generate an instagram post for the topic below.
    topic:
    {state['topic']}

    Requirements:
    - Engaging and visual language
    - 2 to 3 short paragraph (150 -200 words max)
    - Include relevenat emojis
    - End with 5-8 relevant hashtags
    - Casual, firendly tone
    - Call-to-action to engage with the post

    Make it perfect for Instagram's audience
    """
    print('generating instagram post')
    print(prompt)
    response = llm.invoke(prompt).content 
    print('instagram generated')
    return {
        "instagram_post":response
    }

# Generate twitter post
def generate_twitter(state:SocialState)->SocialState:
    prompt = f"""
    Generate a twitter post for the topic below.
    topic:
    {state['topic']}

    Requirements:
    - Maximum  280 characters (this is crucial)
    - Punchy and attention=grabbing
    - Including 2-3 relevant hashtags
    - Conversational tone
    - Can use emojis sparingly
    - Should spark engagement/replies

    Make it perfect for Twitter's fast-paced environment.

    """

    print('generating Twitter post')
    print(prompt)
    response = llm.invoke(prompt).content 
    print('Twitter generated')

    return {
        "twitter_post":response
    }

#generate facebook post
def generate_facebook(state:SocialState)->SocialState:
    prompt = f"""
    Generate a facebook post for the topic below.
    topic:
    {state['topic']}

    Target audience: young professionals
    Tone: inspirational and uplifting

    Include:
    - A powerful opening line
    - A short relatable story or idea
    - Encouragement
    - A call-to-action asking readers to share their experience

    Keep it emotionally engaging.

    """

    print('generating Facebook post')
    print(prompt)
    response = llm.invoke(prompt).content 
    print('Facebook generated')

    return {
        "facebook_post": response
    }

#merge all social media post
def generate_output(state:SocialState)->SocialState:
    output_summary = f""" 
    {'*'*50}
    SOCIAL MEDIA POST SUMMARY
    {'*'*50}

    TOPIC:
    {state['topic']}


    {'='*50}
    INSTAGRAM POST
    {'='*50}
    {state['instagram_post']}


    {'='*50}
    TWITTER POST
    {'='*50}
    {state['twitter_post']}


    {'='*50}
    FACEBOOK POST
    {'='*50}
    {state['facebook_post']}

    """
    return {
        "final_output":output_summary
    }



graph = StateGraph(SocialState)

graph.add_node("instagram",generate_instagram)
graph.add_node("twitter", generate_twitter)
graph.add_node("facebook", generate_facebook)
graph.add_node("final_output", generate_output)

graph.add_edge(START, "instagram")
graph.add_edge(START, "twitter")
graph.add_edge(START, "facebook")

graph.add_edge("instagram","final_output")
graph.add_edge("twitter","final_output")
graph.add_edge("facebook","final_output")

graph.add_edge("final_output", END)

app = graph.compile()

# execute the topic to generate posts for
result = app.invoke({
    "topic": "Lagos hustle"
})

#print out the generate results
print(result['final_output'])

