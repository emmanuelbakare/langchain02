from typing import TypedDict
from langgraph.graph import StateGraph, START,END
from langgraph.types import RetryPolicy
import random

#***** How It works
# RetryPolicy (
#     max_attempts =  5, # int: number of times to retry
#     initial_interval = 2, #float: secs how long to wait before next retry
#     backoff_factor  = 2,  #float: a multiplier for the interval - if first interval is 2, next interval will be 4, then 8...
#     max_interval = 128,  # number of interval should not be more than 128sec
#     jitter = True # it randomizes the retries so that multiple attempts to the server will not be firing at same time. eg. if it fire at 2sec another may fire at 2.3sec
#     retry_on = TimeoutError    #this specify the error your want to retry on. multiple error will require a tuple (TimeOutError, ConnectionError)

# )

class WeatherState(TypedDict):
    city: str
    temperature: float 
    conditions: str 

class APIError(Exception):
    """Simulate Error"""
    pass 

def fetch_weather(state:WeatherState):
    city = state['city']

    """Simulate Request"""
    if random.random() < 0.7:
        print(f"API call failed for {city}")
        raise APIError(f"Weather API Timeout or {city}")
    
    print(f"Successfully fetched for {city}")

    temp = round(random.uniform(15,30),1)
    conditions = random.choice(["Sunny", "Cloudy", "Rainy", "Partially Cloudy"])

    return {
        "temperature": temp,
        "conditions": conditions
    }

def format_result(state:WeatherState):
    print(f"Weather Report for {state['city']}")
    print(f"Temperature: {state['temperature']}")
    print(f"Condition: {state['conditions']}")

builder =StateGraph(WeatherState)

builder.add_node(
    "fetch_weather",
    fetch_weather,
    retry_policy= RetryPolicy(
        max_attempts = 5,
        initial_interval = 1,
        backoff_factor = 2.0,
        max_interval = 10.0,
        jitter = True,
        retry_on =APIError

    ))

builder.add_node(format_result)

builder.add_edge(START, "fetch_weather")
builder.add_edge("fetch_weather", "format_result")
builder.add_edge("format_result", END)

graph = builder.compile()

initial_state = {
    "city":"Lagos",
    "temperatur": 0.0,
    "condition":''
}

try:
    result = graph.invoke(initial_state)
    print(f"\n Final Result: {result}")
except Exception as e:
    print(f"All retry attempts exhausted: e")