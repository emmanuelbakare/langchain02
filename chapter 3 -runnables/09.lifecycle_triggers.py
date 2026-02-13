#get lifecycle of chains on_start, on_error, on_end triggers
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tracers.schemas import Run

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("Give me a very short, simple fact about {topic}")

fact_chain = prompt | model | StrOutputParser()

#define function for on_start listener 
def my_listener_on_start(run:Run):
    """log when the chain starts"""
    print(f"Listener START for '{run.name}' (RUN ID: {run.id})")
    print(f" INPUTS: {run.inputs}")
    print(f"Parent Run ID: {run.parent_run_id}")
    print(f"Tags: {run.tags}, Metadata: {run.extra.get('metadata')}")

#define function for on_end listener 
def my_listener_on_end(run:Run):
    """log when the chain end"""
    print(f"Listener END for '{run.name}' (RUN ID: {run.id})")
    print(f" OUTPUT TYPE: {type(run.output).__name__}, OUTPUT Value: {run.outputs}")
    print(f"Parent Run ID: {run.parent_run_id}")
    print(f"Tags: {run.tags}, Metadata: {run.extra.get('metadata')}")

# call the with_listeners method to add the listener function to the chain
fact_chain_with_listeners =  fact_chain.with_listeners(
    on_start=my_listener_on_start,
    on_end= my_listener_on_end
)

result = fact_chain_with_listeners.invoke({
    "topic":"Soccer"
})

print(f"Final Result: {result}")
print("*"*60)
