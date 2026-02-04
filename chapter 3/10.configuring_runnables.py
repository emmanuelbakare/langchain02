from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.tracers.schemas import Run
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_template("Give a very short fact about {topic}")
model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

base_chain = prompt | model | parser 

def my_listener_on_start(run:Run):
    """log when the chain starts"""
    print(f"Listener START for '{run.name}' (RUN ID: {run.id})")
    print(f" INPUTS: {run.inputs}")
    print(f"Parent Run ID: {run.parent_run_id}")
    print(f"Tags: {run.tags}, Metadata: {run.extra.get('metadata')}")

chain_with_listener = base_chain.with_listeners(
    on_start=my_listener_on_start
)

my_runnable_configuration = RunnableConfig(
    run_name = "Configuration Demo",
    tags = ["single_run_tag","demo_invoke"],
    metadata={
        "user_id": "390aj095j0a9sg",
        "source": "manual test",
        "input_topic_type": "history"
    }
)

# print("=========Demo 1: Per-Invocation Configuration----------")

# per_invoke_result = chain_with_listener.invoke(
#     {
#         "topic": "The Roman Empire"
#     },
#     config=my_runnable_configuration
# )

# print(f"Result: {per_invoke_result}")



#Demo 2: Per-Persistent Configuration

my_persistent_configuration = RunnableConfig(
    run_name = "Persistent Config Demo",
    tags = ["persistent_tag","demo_invoke"],
    metadata={
        "user_id": "390aj095j0a9sg",
        "source": "manual test",
        "input_topic_type": "animal"
    }
)

persistent_chain = chain_with_listener.with_config(
    my_persistent_configuration
)


print("=========Demo 2: Persistent Configuration----------")

persistent_result = persistent_chain.invoke({
    "topic":"Universities"
})

print(f"Result: {persistent_result}")