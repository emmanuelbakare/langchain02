from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()


llm = ChatOpenAI(model="gpt-4o")

async def stream_response_events():
    prompt= "Tell me about the moon"
    event_limit = 0
    async for event_chunk in llm.astream_events(prompt, version="v2"):
        event_limit +=1
        if event_limit >=10:
            print()
            print("...Event Streaming done...")
            return
        
        # this code is to get specific number of character from the stream e.g 5 chunks
        # if event_chunk['event'] == 'on_chat_model_stream':
        #     print(event_chunk['data']['chunk'].content, end="")
        print(event_chunk)

asyncio.run(stream_response_events())

