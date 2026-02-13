from langchain_core.runnables import RunnableLambda
from typing import Any, Dict
import json
from langchain_core.tracers.schemas import Run 

def failing_function(input_dict:Dict[str,Any])-> str:
    topic = input_dict.get("topic","unknown")
    lower_topic = topic.lower()
    if "error" in lower_topic:
        raise ValueError(f"Intentional Error triggered by topic: {topic}")
    elif "network" in lower_topic:
        raise ConnectionError("Simulated network connection failure")
    elif "json" in lower_topic:
        bad_json = '{"Imcomplete": json'
        return json.loads(bad_json)
    else:
        return f"Processing topci:{topic}"
    
error_runnable = RunnableLambda(failing_function)

def my_error_listener(run:Run):
    print(f"Run ID: {run.id}")
    print(f"Run Name: {run.name}")
    print(f"Start Time: {run.start_time}")
    print(f"End Time: {run.end_time}")
    print(f"Inputs: {run.inputs}")
    print(f"Outputs: {run.outputs}")

    print("---- Error Details---")
    print(run.error)


error_runnable_with_listener = error_runnable.with_alisteners(
    on_error=my_error_listener
)

print("----- Demo: Running Error Scenerio------")

try:
    result = error_runnable_with_listener.invoke({
        "topic":"Error somewhere here"
    })
    print(f"Result:{result}")
except Exception as e:
    print("An error occurred")



 
    