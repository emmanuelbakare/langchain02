"""
This subagent will be 
specilize in searching and recommending flight

It will hanfle natural language queries about flight options, prices and schedules

ACTIONS - to do the above. It creates
- Search flight function
- Compare Flight Price function
"""


# if your subagents are simple ReAct Agent just use create_agent instead of doing langgraph implementations
#in other words, if what you need is a simple agent, use langchain create_agent, you dont need the langgraph long process
from langchain.agents import create_agent   
from langchain.tools import tool
from tools.mock_data import get_flights


@tool
def search_flight(destination:str, 
                  budget_max:int |None = None, 
                  preferred_stops: str = "any")->str:
    """
    Search for available flights to a destination

    Args:
        destination: The destination city (e;g "Tokyo", "Paris"...)
        budget_max: Maximum budget per person in USD (optional)
        preferred_stops: "direct", "one-stop", or "any"

    Returns:
        Available flight options with details
    """
    flights = get_flights(destination)

    if not flights:
        return f"No flight found for our {destination}, please check the destination name."
    
    #Filter the flight by budget

    if budget_max:
        flights  = [f for f in flights if f['price'] <= budget_max]

    # Filter by stops - direct stop is 0 stops
    if preferred_stops =="direct":
        flights = [f for f in flights if f['stops'] ==0]
    elif preferred_stops == "one-stop":
        flights = [f for f in flights if f['stops'] ==1]

    if not flights:
        return "No Flights match your criteria. Try adjusting your budject or stop preferences"
    
    # Format and Build result
    results = [f"Found {len(flights)} flights to {destination}: \n"]

    for flight in flights:
        result= f"""
        * {flight['airline']} {flight['flight_number']}
        Route: {flight['departure_city']} -> {flight['arrival_city']}
        Departure: {flight['departure_time']} Arrival {flight['arrival_time']}
        Duration: {flight['duration']} | Stops {flight['stops']} {'('+flight.get('layover','')+ ')' if flight.get('layover') else '(Direct)'}
        Price: ${flight['price']} USD ({flight['class']})
        """
        results.append(result)
    
    return "\n".join(results)

@tool
def  compare_flight_prices(destination:str)->str:
    """
    Compare prices accros all available flights to a destination.

    Args:
        destination: The destination city

    Returns:
        Price comparison summary with cheapest and recommended options
    """
    flights = get_flights(destination)

    if not flights:
        return f" No flight found to {destination}"
    
    #Sort by price
    sorted_flights = sorted(flights, key = lambda x: x['price'])
    cheapest = sorted_flights[0]

    # Find the best value (Direct flight with good price)
    direct_flights = [f for f in flights if f['stops']==0]
    #if there is direct_flight then get the min from the list in direct_flight. If there is nothing in direct_flight use the cheapest flight
    best_value = min(direct_flights, key=lambda x: x['price']) if direct_flights else cheapest

    result = f"""
        Flight Comparison to {destination}

        CHEAPEST OPTIONS:
        {cheapest['airline']} {cheapest['flight_number']} - ${cheapest['price']}
        {cheapest['duration']} | {'Direct' if cheapest['stops']==0 else cheapest['stops']} stops(s)

        BEST VALUE:
        { best_value['airline']} {best_value['flight_number']} - ${best_value['price']} 
        {best_value['duration']} | Direct Flight

        Price Range: ${sorted_flights[0]['price']} - ${sorted_flights[-1]['price']}
    """



FLIGHT_AGENT_PROMPT = """
    You are a flight searchj specialist. Your job is to help users find the best flights for their trip.

    Your capabilities:
    - Search for available flights to any destination
    - Compare prices acrsoss different airlines
    - Fliter by budgetm number of stops, and preferences
    - Recommend the best options based on user needs

    When responding:
    1. Always search for flights first using the search_flight tools
    2. Consider the user's budget constraints if mentioned
    3. Highlights the trade-offs between prices, duratioin, and convenience
    4. Recommend specific flights based on the user;s priorities
    (cheapest, fastest, most convenient)

    Be concise but informative. Focus onactionable recommendations.
"""

def create_flights_agent(model):

    return create_agent(
        model,
        tools = [search_flight, compare_flight_prices],
        system_prompt=FLIGHT_AGENT_PROMPT
        
    )