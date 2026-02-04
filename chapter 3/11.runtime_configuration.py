from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig, ConfigurableField
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_template("Give a very short fact about {topic}")

model = ChatOpenAI(model="gpt-4o-mini").configurable_fields(
    max_tokens=ConfigurableField(
        id="llm_token_cap", # can be any name
        name = "LLM Maximum Response Token",
        description= "Maximum number of tokens to be used for response"
    )
)

parser = StrOutputParser()

base_chain = prompt | model | parser 

# demo 1 : Default action
print("------ Invoking with Default token Limit------------")
result_default = base_chain.invoke({"topic":" the sun"})
print(f"Facts about the sun (Max Token Default): {result_default}")


#demo 2: Configure low token
print("------ Invoking with a Low  token Limit------------")
low_token_config =RunnableConfig(
    configurable={
        "llm_token_cap":10
    }
    
)
result_low_token = base_chain.invoke({
    "topic":" the sun"},
    config=low_token_config)
print(f"Facts about the sun (Max Token =10 ): {result_low_token}")