"""
- a node that retrieves and put them in state
- A chatbot nmode, that responde using the treived memories
- a node that takes the current conversation, and extract new memories
"""

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.embeddings import init_embeddings
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from typing import TypedDict, Annotated
from operator import add
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model = "gpt-4o-mini")

class ChatMessagesState(TypedDict):
    messages : Annotated[list, add]
    memory_context : str 

#memory retrieval node

def retrieve_memories(state:ChatMessagesState, config:RunnableConfig, store:BaseStore):

    #get user_id from config
    user_id = config["configurable"].get("user_id", "defailt_user")

    print(f"\n {'='*70}")
    print("MEMORY RETRIEVAL NODE")
    print('='*70)

    #search for memories
    user_memories_namespace = (user_id,"memories")

    memories = store.search(
        user_memories_namespace,
        query = "what are the fact about this user?"
    )

    memory_context =""
    if memories:
        print(f" Found  {len(memories)} memories" )
        memory_texts = []
        for i, memory in enumerate(memories, 1):
            text = memory.value.get("text", "")
            print(i, text)
            memory_texts.append(text)

        memory_context = "\n".join([f"- {text}" for text in memory_texts])

    else:
        print("NO MEMORIES FOUND FOR (NEW USER)")
    
    print('='*70)

    return {
        "memory_context": memory_context
    }


# Chatbot node
def chatbot(state: ChatMessagesState, config: RunnableConfig):
    user_id = config["configurable"].get("user_id","default_user")

    print(f"\n {'='*70}")
    print("CHATBOT NODE")
    print('='*70)

    memory_context = state.get("memory_context", "")\
    
    if memory_context:
        print(" Using retrieved memories for personalization")

        system_prompt = f"""
        You are a helpful assistant with moenry of past conversation

        what you  remember about this user:
        {memory_context}

        Use this ifnrmation to personalize your response. Be natural, and conversational
"""
    else:
        print("No memory context available")
        system_prompt = f"""
        You're a helpful assistant. This is your first conversation with this user

        """

    messages = [
        SystemMessage(content=system_prompt),
        *state["messages"]
    ]

    # Generate Response
    response = llm.invoke(messages)

    print(f"\n Response Generated: {response.content[:80]}...")
    print('='*70)

    return {
        "messages": [response]
    }



# Memory Extraction Node

def extract_and_save_memory(state:ChatMessagesState, config: RunnableConfig, store:BaseStore):

    user_id = config["configurable"].get("user_id","default_user")

    print(f"\n {'='*70}")
    print("MEMORY EXTRACTION NODE")
    print('='*70)
    print(f"Extracting memories for user: {user_id}")

    if len(state["messages"]) >= 2:
        user_message = state['messages'][-2].content
        assistant_message = state["messages"][-1].content
    else:
        print("Not enough message to extract from")
        print(f"{'='*70}\n")
        return state

    print(f"User Said: {user_message[:60]}...")    
    print(f"Assistant Said: {assistant_message[:60]}...")    

    print("\n EXTRACTING FACTS...")

    extract_prompt =f"""Look at this conversation and extract any facts worth remembering about the user
    user: {user_message}
    Assistant: {assistant_message}

    List each fact ona new line starting with a dash (-).
    Only include clear, factial information about the USER (not about the assistant)
    If there are no fact to remember, response with: NONE

    Example of God Facts:
    - User's name is Alice
    - User workds as a teacher
    - User enjoys hiking
    - User is learning Python

    Exmaples of bad facts (Don't include these):
    - The assistant was helpful
    -  we had a conversation
    - The user asked a question
    """

    extraction = llm.invoke(extract_prompt).content

    print(f"Extraction result {extraction[:80]}...")

    print(" SAVING TO STORE...")

    if "NONE" not in extraction.upper():
        #split each facts into a list item
        lines = [line.strip() for line in extraction.split("\n") if line.strip().startswith("-")]
        save_count = 0 
        for line in lines:
            fact = line[1:].strip() #remove the dash before each item

            if fact and len(fact) > 5:
                memory_key = f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

                store.put(
                    namespace=(user_id, "memories"),
                    key= memory_key,
                    value = {
                        "text":fact,
                        "timestamp": datetime.now().isoformat(),
                        "source": "conversation"
                    }
                )
                print(f"Saved: {fact}")
                save_count = 1
            
            if save_count ==0:
                print("No valid factos to save")
    else:
        print(f"No new facts to save")

    print('='*70,'\n')

    # return state
    return {}



#build graph

builder = StateGraph(ChatMessagesState)

builder.add_node(retrieve_memories)
builder.add_node(chatbot)
builder.add_node("extract_memories",extract_and_save_memory)

builder.add_edge(START, "retrieve_memories")
builder.add_edge("retrieve_memories", "chatbot")
builder.add_edge("chatbot","extract_memories")

checkpointer = MemorySaver()

store_embeddings_model = init_embeddings("openai:text-embedding-3-small")

store = InMemoryStore (
    index ={ 
        "embed": store_embeddings_model,
        "dims": 1536,
        "fields": ["text","$"]
    }
)

graph = builder.compile(
    checkpointer=checkpointer,
    store = store 
)

config = {
    "configurable":{
        "thread_id": "chat001",
        "user_id" : "sarah"
    }
}

#Turn 1: Introduction
print('\n', '='*70)

sara_message_1 = "Hi my name is Sarah and I'm a data scientist"

result = graph.invoke(
    {
        "messages":[HumanMessage(content=sara_message_1)]
    },
    config = config
)

print(f"\nUSER: {sara_message_1}")
print(f"ASSISTANT: {result['messages'][-1].content}")





#Turn 2: Project
print('\n', '='*70)

sarah_message_2 = "I'm currently working on a manchine learnming project using Python and TensorFlow"

result = graph.invoke(
    {
        "messages":[HumanMessage(content=sarah_message_2)]
    },
    config = config
)

print(f"\nUSER: {sarah_message_2}")
print(f"ASSISTANT: {result['messages'][-1].content}")



#Turn 3: Share Hobbies
print('\n', '='*70)

sarah_message_3 = "In my free time, I love playing guiter and going on weekend hikes"

result = graph.invoke(
    {
        "messages":[HumanMessage(content=sarah_message_3)]
    },
    config = config
)

print(f"\nUSER: {sarah_message_3}")
print(f"ASSISTANT: {result['messages'][-1].content}")



#Turn 4: Share Dietary preferences
print('\n', '='*70)

sarah_message_4 = "I'm vegetarian and I prefer coffee over tea."

result = graph.invoke(
    {
        "messages":[HumanMessage(content=sarah_message_4)]
    },
    config = config
)

print(f"\nUSER: {sarah_message_4}")
print(f"ASSISTANT: {result['messages'][-1].content}")


#Inspect the memory store

print("\n\n","="*70)
print('INSPECTING STORED MEMORIES')
print("="*70)

memories = store.search(
    ("sarah","memories"),
    query = "What are the facts about this user?"
)

print(f"\n Total memories stored for Sarah: {len(memories)}n")

for i, memory in enumerate(memories, 1):
    print(f"{i}. {memory.value['text']}")
    print(f"Key: {memory.key}")
    print(f"Timestamp: {memory.value['timestamp']}")
    print(f"Source: {memory.value['source']}")
    print(f"Created At: {memory.created_at}\n")