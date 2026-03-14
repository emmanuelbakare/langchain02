"""
Supervisor Agent

The main orchestrating agent that coordinates specialized subagents to create comprehensive travel plans.

This implements the SubAgents pattern where:
- Supervisor receives user requrest and makes routing decisions
- Subagents are wrapped as tools for the supervisor to call
- Results flow back to supervisor for synthesis

"""

from langchain.agents import create_agent
from langchain.tools import tool 
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from subagents import (
    create_flights_agent,
    create_hotels_agent,
    create_activities_agent,
    create_itinerary_agent
)

_agents = None

def initialize_agents(model_name:str="openai:gpt-4o-mini"):
    """ Initialize the model and all subagents"""

    model = init_chat_model(model_name)

    return {
        "model": model,
        "flights_agent":create_flights_agent(model),
        "hotels_agent": create_hotels_agent(model),
        "activities_agent": create_activities_agent(model),
        # "create_itinerary_agent": create_itinerary_agent(model)
        "itinerary_agent": create_itinerary_agent(model)
    }

def get_agents():
    """Get or initialize agents"""
    global _agents
    if _agents is None:
        _agents = initialize_agents()
    
    return _agents


# Wrap each subagent in a Tool
@tool
def search_flight(request:str)->str:
    """Search for flight to a destination
    
    Use this when the user needs to find flights. pass the full context including
    - Destination city
    - Travel dates (if mentioned)
    - Budget constraints (if mentioned)
    - Preference (direct lfight, specific airlines, etc)
    
    Example: "Find flights to Tokyo, budget around $800, prefer direct flights
    """

    agents = get_agents()

    result = agents['flights_agent'].invoke({
        "messages":[{"role": "user","content": request}]
    })

    return result["messages"][-1].text


@tool
def search_hotels(request:str)->str:
    """
    Search for hotels and accommodation

    Use this when the user needts to find places to stay. Pass the full context including
    - Destination city
    - Traveler Type (solo, couple, famuly etc.)
    - Budget per nigt (if mentioned)
    - Preferences (amenities, location etc)

    Example: "Find family-friendly hotels in Tokyo, budget $200/night, need pool
    """
    agents = get_agents()

    result = agents['hotels_agent'].invoke({
        "messages":[{"role":"user", "content":request}]
    })
    
    return result["messages"][-1].text



@tool 
def search_activities(request:str)->str:

    """ 
    Search for things to do , attraction, and restaurants.

    use this when the user wants to discover activities, experiences, or dining options
    pass the full context including:
    - Destination city
    - Interest (culture, food, nature, adventure, etc.)
    - Trip style (relaxed, packed, foodie,etc.)
    - Any specific requests

    Example: "Find Cultural activities and good sushi restraurants in Toyko
    """

    agents = get_agents()

    result = agents['activities_agent'].invoke({
        "messages":[{"role":"user", "content":request}]
    })

    return result["messages"][-1].text



@tool
def create_itinerary(request:str)->str:
    """
    Create an organize a trip itinerary.

    Use this to organize flight, hotels, and activities into a cohesive plan.
    pass the full context including:
    - All selected components (flight, hotel, activities)
    - Number of days
    - Trip pace preference (relaxed, moderate, packed)
    - Any scheduling preference

    Example: "Create a 5-day Tokyo itinerary with the selected hotel and activities
    """
    agents = get_agents()

    result = agents['itinerary_agent'].invoke({
        "messages":[{"role":"user", "content":request}]
    })

    return result["messages"][-1].text


SUPERVISOR_PROMPT = """
You are a professional travel panning assitant. Your job is to help users plan their perfect trip by coordinating specialized travel experts.

You have access to four specialist tools
1. search_flight - find and compare flight options
2. search_hotels - find accommodation matching preferences
3. search_activities - Discover things to do, attractions, and restaurants
4. create_itinerary - Organize everything into a day-by-day- plan

WORKFLOW GUIDELINES:

For a complete trip planning request:
1. First, understand the user's needs (destination, dates, travelers, budget, interests)
2. Search for light to get tranvel options
3. Serch for hotels matching their traveler type and budget
4. search for activities based on their interests.
5. Create an itinerary to organize everything

For partial request (e.g., "just find hotels"):
- Only call the relevant specialist
- Dont overwhelm with unnecessary informaiton

RESPONSE GUIDELINE:

- Be conversational and helpful, not robotic
- Summarize hey findings clearly
- Make specific recommendation when you have enought information
- Ask clarifying questions if the request if vague
- Present options in a scannable format
- Always consider the user's budget and preferences

When synthesizing result from multiple specialist:
- Use the create_itinerary tool to format and display your final result
- Highlight the best march for their needs
- Note any trade-offs they should consider
- Provide a cohesive recommendation, not just raw data

Remember: You're knowledgeable travel advisor, not just a search engine.
Add value by making thoughtful recommendations based on the user's specific situation
"""


def create_supervisor_agent(model_name: str = "openai:gpt-4o-mini", 
                            user_memory:bool=True):
    """
    Create and return the supervisor agent

    Args:
    model_name: The model to use for the supervisor
    user_memory: Whether to enable conversation menory (checkpointing)
    """

    global _agents
    _agents = initialize_agents(model_name)

    supervisor = create_agent(
        _agents["model"],
        tools = [search_flight, search_hotels, search_activities, create_itinerary],
        system_prompt=SUPERVISOR_PROMPT,
        checkpointer= InMemorySaver() if user_memory else None
    )

    return supervisor