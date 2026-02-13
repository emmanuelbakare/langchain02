from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

president_schema ={
    "name": "getInfo",
    "description":"Get Country President Information",
    "parameters":{
        "type": "object",
        "properties":{
            "name":{
                "type":"string",
                "description": "The name of the president"
            },
            "country":{
                "type":"string",
                "description": "The country of the president"
            },
            "age":{
                "type":["integer", "null"],
                "description": "The age of the president"
            },
            
        },

        "required":["name","country"]
        

    }
}

structured_llm = llm.with_structured_output(president_schema)

response = structured_llm.invoke("Who is the president of Nigeria")

print(response)