import operator
from typing import TypedDict, Annotated, Optional

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END


# -----------------------------
# Pydantic Structured Output
# -----------------------------
class TweetEvaluation(BaseModel):
    score: int = Field(
        description="Overall quality score from 1 (worst) to 10 (best)"
    )
    feedback: str = Field(
        description="Detailed feedback explaining how to improve the tweet to be funnier, sharper, and more viral"
    )


# -----------------------------
# Graph State
# -----------------------------
class GraphState(TypedDict):
    topic: str
    tweet: Optional[str]
    score: Optional[int]
    feedback: Optional[str]
    iteration: int


# -----------------------------
# LLM Initialization
# -----------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.9,
)


# -----------------------------
# Node 1: Generate Tweet
# -----------------------------
def generate_tweet(state: GraphState) -> GraphState:
    topic = state["topic"]
    feedback = state.get("feedback")
    iteration = state.get("iteration", 0)

    if feedback:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a world-class Twitter content creator. "
                    "Create highly engaging, witty, concise tweets optimized for virality.",
                ),
                (
                    "user",
                    "Topic: {topic}\n\n"
                    "Previous feedback to improve the tweet:\n"
                    "{feedback}\n\n"
                    "Generate a significantly improved tweet. "
                    "Make it sharper, funnier, and more viral. "
                    "Keep it under 280 characters.",
                ),
            ]
        )
        chain = prompt | llm
        response = chain.invoke(
            {"topic": topic, "feedback": feedback}
        )
    else:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a world-class Twitter content creator. "
                    "Create highly engaging, witty, concise tweets optimized for virality.",
                ),
                (
                    "user",
                    "Topic: {topic}\n\n"
                    "Generate a funny, insightful, and potentially viral tweet. "
                    "Keep it under 280 characters.",
                ),
            ]
        )
        chain = prompt | llm
        response = chain.invoke({"topic": topic})

    return {
        "tweet": response.content.strip(),
        "iteration": iteration + 1,
    }


# -----------------------------
# Node 2: Reflect & Score
# -----------------------------
def reflect_and_score(state: GraphState) -> GraphState:
    tweet = state["tweet"]

    structured_llm = llm.with_structured_output(TweetEvaluation)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a viral Twitter growth expert. "
                "Evaluate tweets for humor, originality, clarity, emotional impact, "
                "and viral potential.",
            ),
            (
                "user",
                "Evaluate the following tweet:\n\n"
                "{tweet}\n\n"
                "Grade it from 1 to 10.\n"
                "1 = terrible, not funny, no viral potential.\n"
                "10 = extremely funny, highly engaging, strong viral potential.\n\n"
                "Provide specific improvement feedback.",
            ),
        ]
    )

    chain = prompt | structured_llm
    evaluation: TweetEvaluation = chain.invoke({"tweet": tweet})

    return {
        "score": evaluation.score,
        "feedback": evaluation.feedback,
    }


# -----------------------------
# Conditional Edge Logic
# -----------------------------
def should_continue(state: GraphState):
    score = state["score"]
    iteration = state.get("iteration", 0)

    # Safety stop after 5 iterations
    if iteration >= 5:
        return END

    if score is not None and score >= 8:
        return END
    else:
        return "generate"


# -----------------------------
# Build LangGraph
# -----------------------------
builder = StateGraph(GraphState)

builder.add_node("generate", generate_tweet)
builder.add_node("reflect", reflect_and_score)

builder.set_entry_point("generate")

builder.add_edge("generate", "reflect")

builder.add_conditional_edges(
    "reflect",
    should_continue,
    {
        "generate": "generate",
        END: END,
    },
)

graph = builder.compile()


# -----------------------------
# Example Invocation
# -----------------------------
if __name__ == "__main__":
    result = graph.invoke(
        {
            "topic": "Remote work and productivity",
            "tweet": None,
            "score": None,
            "feedback": None,
            "iteration": 0,
        }
    )

    print("Final Tweet:\n", result["tweet"])
    print("\nFinal Score:", result["score"])
    print("\nFeedback:\n", result["feedback"])