from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

# ----------------------------
# LLM Configuration
# ----------------------------
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.9
)

# ----------------------------
# State Definition
# ----------------------------
class TweetState(TypedDict):
    topic: str
    tweet: str
    feedback: str
    score: int

# ----------------------------
# Prompt Templates
# ----------------------------

generate_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a viral Twitter content creator.
Create a highly engaging, witty, funny, and potentially viral tweet.
Keep it under 280 characters.
Make it sharp, clever, and shareable.
If feedback is provided, improve the tweet based on that feedback."""
        ),
        (
            "human",
            """Topic: {topic}
Previous feedback (if any): {feedback}
Generate the improved tweet:"""
        ),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a viral Twitter growth expert and humor analyst.
Evaluate the tweet based on:
1. Humor
2. Virality potential
3. Engagement likelihood
4. Clarity and punch

Return your response strictly in JSON format:
{
  "score": <integer 1-10>,
  "feedback": "<clear actionable improvement suggestions>"
}

Be critical. Only give 8 or above if it's genuinely strong and viral-worthy."""
        ),
        (
            "human",
            """Tweet:
{tweet}"""
        ),
    ]
)

generate_chain = generate_prompt | llm | StrOutputParser()
reflection_chain = reflection_prompt | llm | StrOutputParser()

# ----------------------------
# Node Definitions
# ----------------------------

def generate_tweet(state: TweetState) -> TweetState:
    tweet = generate_chain.invoke(
        {
            "topic": state["topic"],
            "feedback": state.get("feedback", "")
        }
    )
    return {
        **state,
        "tweet": tweet
    }


def reflect_tweet(state: TweetState) -> TweetState:
    reflection_raw = reflection_chain.invoke(
        {
            "tweet": state["tweet"]
        }
    )

    try:
        reflection_json = json.loads(reflection_raw)
        score = int(reflection_json["score"])
        feedback = reflection_json["feedback"]
    except Exception:
        score = 5
        feedback = "Evaluation parsing failed. Improve humor, clarity, and punch."

    return {
        **state,
        "score": score,
        "feedback": feedback
    }


# ----------------------------
# Conditional Edge Logic
# ----------------------------

def should_regenerate(state: TweetState) -> Literal["regenerate", "end"]:
    if state["score"] >= 8:
        return "end"
    return "regenerate"


# ----------------------------
# Build LangGraph
# ----------------------------

builder = StateGraph(TweetState)

builder.add_node("generate", generate_tweet)
builder.add_node("reflect", reflect_tweet)

builder.set_entry_point("generate")

builder.add_edge("generate", "reflect")

builder.add_conditional_edges(
    "reflect",
    should_regenerate,
    {
        "regenerate": "generate",
        "end": END,
    },
)

graph = builder.compile()

# ----------------------------
# Example Usage
# ----------------------------

if __name__ == "__main__":
    result = graph.invoke(
        {
            "topic": "AI taking over daily life",
            "tweet": "",
            "feedback": "",
            "score": 0,
        }
    )

    print("\nFinal Tweet:\n")
    print(result["tweet"])
    print("\nFinal Score:", result["score"])