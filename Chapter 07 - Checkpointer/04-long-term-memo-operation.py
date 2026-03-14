# 1.  Initialize A Store

from langgraph.store.memory import InMemoryStore
memory_store = InMemoryStore()

# 2. Store Memory
import uuid
"""
Parameters needed to construct a memory store incluide
a. namespace
b. key
c. value (dict)
"""

user_preferecenes_namespace = ("user_123","preferences")
memory_key = str(uuid.uuid4())
memory = {
    "fact":"I like eating rice"
}

# store the memory using a put method.  Add namespace, key, value
memory_store.put(
    namespace=user_preferecenes_namespace,
    key= memory_key,
    value= memory
)

# or

memory_store.put(
    user_preferecenes_namespace,
    memory_key,
    memory
)

# 3. Retrieve Items from the Store

#retrive entire memory in a namespace
memories = memory_store.search(
    user_preferecenes_namespace
)

#to return a single memory use the get method, you have to provide the namespace and key
single_memory = memory_store.get(
    user_preferecenes_namespace,
    memory_key
)

# 4. List namespaces

my_namespace  = memory_store.list_namespaces() #list all name spaces
#below list namespace that start with a and b e.g ('a','b', 'c') or ('a','b', 'd','j') etc
my_namespace  = memory_store.list_namespaces(prefix=("a","b")) 
#this works like above but it not return name space that is higher than 3 item e.g will not return ('a','b', 'd','j')
my_namespace  = memory_store.list_namespaces(prefix=("a","b"), max_depth=3) 


# 5. Delete namespace
memory_store.delete(
    namespace= user_preferecenes_namespace,
    key= memory_key
)

# 6.  Semantic Memory
"""
semantic search does not have ot be exact search. e.g you can have stored values like facts about me. 
but the search query ask ' do I like swimming', the system should be able do deduce that the query is refering to
one of the items in what I like.

- embedding model is the index to first set
- then field property  that provides a list of key of what you want to search 
"""
from langgraph.store.memory import InMemoryStore

store = InMemoryStore(
    index= {
        "embed": init_embeddings("openai:text-embedding-3-small") #
        "fields": ["fact", "$"], #search for facts and any other thing if you do ['fact'] it will only search for fact the '$' is for the any other thing
        "dims": 1536 # there are other dimension
    },
)

store.search(
    user_preferecenes_namespace,
    query ="what does emmanuel like?"
)