from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

#define tools
@tool 
def get_weather(city:str)->str:
    """get the weather for a city"""

    weather_data = {
        "New York": "Sunny, 72 F",
        "London": "Cloudy, 15 F",
        "Tokyo": "Rainy, 20 C"
    }
    
    return weather_data.get(city,"Weather data not available")

@tool 
def calculate_tip(bill_amount:float, tip_percentage: float):
    """Calculat tip amount based on bill and percentage"""

    return round(bill_amount *(tip_percentage/100),2)

llm = ChatOpenAI(model="gpt-4o")

llm_with_tools = llm.bind_tools([
    get_weather,
    calculate_tip
])

weather_prompt = "What's the waether in Tokyo"
tip_amount = "Calculate a 20% tip on a %50 bill"

response =llm_with_tools.invoke(weather_prompt)

#get all tools that was called with tool_calls
tool_calls = response.tool_calls

# print(tool_calls)
# the print return [{'name': 'get_weather', 'args': {'city': 'Tokyo'}, 'id': 'call_PvK9ZIU0OefPBBnx4shTlLt6', 'type': 'tool_call'}]

#get the tool 'name' that was called and pass its 'args' to it to call it
for tool_call in tool_calls:
    if tool_call['name'] =="get_weather":  
        result = get_weather.invoke(tool_call["args"])  # call get_weather(val)
    elif tool_call['name']=="calculate_tip":
        result = calculate_tip.invoke(tool_call["args"]) # call calculate_tip(val)
    else:
        result = "No tool found"

print(result) #returns Rainy, 20 C ... it calls get_weather('tokyo')


