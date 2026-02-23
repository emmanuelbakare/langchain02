from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(model="gpt-4o")

response = llm.invoke("Tell me about NNPC in Nigeria")

# 1. get usage data
print(response.usage_metadata)
"""
Output:
{'input_tokens': 14, 'output_tokens': 500, 'total_tokens': 514, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
"""


#2. get usage data from response_metadata
# print(response.response_metadata["token_usage"])

"""
Output:
{'completion_tokens': 500, 'prompt_tokens': 14, 'total_tokens': 514, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}
"""