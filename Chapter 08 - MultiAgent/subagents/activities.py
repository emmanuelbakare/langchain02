"""
Activity Agent

Specialized Agent for discovering things to do, attractions , and restaurants.
Handles natural language queires about experiences and dining

Tools:
- search_activities
- search_restaurants
- get_activity_recommendations
"""

from langchain.agents import create_agent
from langchain.tools import tool

from tools.mock_data import get_activities, get_restaurants

@tool
def search_activities(
    destination:str,
    interests: list[str] | None = None,
    budget_max: int | None = None 
) -> str:
    """
    Search for activities and attractions in destination.

    Args:
    destination: The destination city (e.g "Tokyo", "paris")
    interest: List of interests like "culture", "food", "nature", "entertainment", "art" (optional)
    budget_max: Maximum budget per activity in USD (optional)

    Return:
        Available activities with details
    """

    activities = get_activities(destination)

    if not activities:
        return f"No activities found in {destination}. Please check the destination name"
    
    #filter by interest
    if interests:
        interest_lower  = [ interest.lower() for interest in interests]

        filtered = []

        for activity in activities:
            if any(interest in [bf.lower() for bf in activity.get("best_for",[])]  for interest in interest_lower):
                filtered.append(activity)
            elif any(interest in activity.get("category", "").lower() for interest in interest_lower):
                filtered.append(activity)
        
        if filtered:
            activities = filtered

    #Filter by budget if specified
    if budget_max:
        activities = [ a for a in activities if a['price'] <= budget_max]

    if not activities:
        return "No activities match your criteria. Try adjusting your interest or budget"
    
    #Format results
    results = [f"Found {len(activities)} activity/activities in {destination}: \n"]

    for activity in activities:
        price_str = f"${activity['price']}" if activity['price'] > 0 else "FREE"

        result = f"""
    {activity['name']}
    Category : {activity['category']}
    Duration : {activity['duration']}
    Price : {price_str}
    Rating :  {activity['rating']}/5
    Lcation : {activity['location']}
    Best for: {', '.join(activity['best_for'])}
    {activity['description']}
    """
        results.append(result)
    
    return  "\n".join(results)



@tool 
def search_restaurants(
    destination:str | None = None,
    cuisine: str | None = None,
    price_range: str | None = None
)->str:
    """
        Search for restaurants and dinning options in a destination.

        Args:
        destination: The destination city (e.g "Tokyo", "paris")
        cuisine: Type of cuisine (e.g. "Sushi", " Raman", French") (Optional)
        price_range: "$","$$","$$$","$$$$" (optional) 
    """

    restaurants = get_restaurants(destination)

    if not restaurants:
        return f" No restaurant data available for {destination}"
    
    #Filter by cuisine if specified
    if cuisine:
        cuisine_lower = cuisine.lower()
        restaurants = [r for r in restaurants if cuisine_lower in r['cuisine'].lower()]

    #Filter by price range id specified

    if price_range:
        restaurants = [r for r in restaurants if r['price_range']==price_range]

    if not restaurants:
        return "No restaurant march your criteria. Try adjusting your filters"
    
    #format Result
    results  = [f" Found {len(restaurants)} restaurants(s)"]

    for restaurant in restaurants:
        result =f""" 
    {restaurant['name']}
    Cousine: {restaurant['cuisine']}
    Price: {restaurant['price_range']}
    Rating: {restaurant['rating']}
    Neighborhood: {restaurant['neighborhood']}
    Best for: {', '.join(restaurant['best_for'])}
    {restaurant['description']}

    """
        results.append(result)

    return "\n".join(results)


@tool 
def get_activity_recommendations(
    destination: str,
    trip_style: str,
    num_days: int = 3
)->str:
    """
    Get curated activities recommendations based on trip style.

    Args:
        destination: The destination city
        trip_style: Style of trip - "cultural","foodie","adventure","relaxation", "family"
        num_days: Number of days for the trip

        Returns:
            Curated list of must-do activities
    """

    activities = get_activities(destination)

    if not activities:
        return  f"No activities found in {destination}"
    
    #Map trip style to relevant interests.
    style_mapping = {
        "cultural":["culture","history","art"],
        "foodie": ["food", "dining"],
        "adventure": [ "nature","outdoor","adventure"],
        "relaxation": ["spa","nature","scenic"],
        "family": ["families","kids", "entertainments"] 
    }
    
    interests = style_mapping.get(trip_style.lower(),["culture","food"])

    #Score activities on relevance
    scored = [] 

    for activity in activities:
        score = 0
        for interest in interests:
            if interest in [bf.lower() for bf in activity.get("best_for",[])]:
                score += 2
            if interest in activity.get("category","").lower():
                score +=1

            score += activity.get("rating",0)
            # scored.append(activity, score)
            scored.append((activity, score))
    
    # Sort by score and get top recommendations
    scored.sort(key=lambda x:x[1], reverse=True)

    top_activities = [a[0] for a in scored[:num_days*2]]

    result = f""" 
    TOP {len(top_activities)} ACTIVITIES for a {trip_style} trip to  {destination}

    """

    for i, activity in enumerate(top_activities,1):
        prince_str = f"${activity['price']}" if activity['price'] > 0 else "FREE"
        result +=f"""{i}. {activity['name']}
        {activity['category']} | {activity['duration']} | {prince_str}
        {activity['description']} 
"""
        
    return result



ACTIVITIES_AGENT_PROMPT= """
You are a local experiences and activities specialist. Your job is to help users discover amazing things to do at their destination.

Your Capabilities:
- Search for activities, attractions, and experiences
- Find restaurants and dining recommendations
- Curate activities based on trip style and interests.
- Provide local insights and tips

When responding:
1. Consider the traveler's interests (culture, food, adventure etc)
2. Mix different types of activities for variety
3. Include both popular attractions and hidden gems
4. Factor in practical details like duration and location
5. Recommend restaurants that match the trip style

Be enthusiastic but practical. Help travelers make the most of their time with specific, actionable recommendations.
Consider logistics - don't recommend activities on opposite sides of the city for the same day.
"""


def create_activities_agent(model):
    return create_agent(
        model,
        tools=[search_activities, search_restaurants, get_activity_recommendations],
        system_prompt=ACTIVITIES_AGENT_PROMPT
    )