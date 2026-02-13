# this code create a cache of the first request so that if the second request is same,
# it will not need to ask the llm again. It will only return the cached response.
from langchain_openai import ChatOpenAI
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

from dotenv import load_dotenv

load_dotenv()

set_llm_cache(InMemoryCache()) # set the catch as an In memory cache

llm = ChatOpenAI(model="gpt-4o")


response1 = llm.invoke("Who is the president of Nigeria")
print(response1.content)
response2 = llm.invoke("Who is the president of Nigeria")
print(response2.content)