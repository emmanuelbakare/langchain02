from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core. runnables import RunnableLambda,RunnableParallel, RunnableBranch
from dotenv import load_dotenv

load_dotenv()

#1. Setup LLM
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

#2. Chain A: Generate concise statement
statement_prompt = ChatPromptTemplate.from_template(
    "Generate a very short, concise sentence about: {topic}"
)

sentence_chain = statement_prompt | model | StrOutputParser()

#3. Chain B: Generate a few keywords, lreated to the same topic

keyword_prompt  = ChatPromptTemplate.from_template(
    "List 3-5 comma-seperated keywords related to:: {topic}. Do not aadd any extra text or intros"
)

keyword_chain = keyword_prompt | model | StrOutputParser()

# --Combine Chains in Parallel

parallel_generation = RunnableParallel(
    sentence = sentence_chain,
    keywords = keyword_chain
)


#--- DEfine Conditional Logic (RunnableBranch)---- 

#5. Custom RunnableLambdas for the consition check

def is_sentence_short(data:dict)->bool:
    """ return True if the generated sentence <== 50 characters, False otherwise"""
    sentence = data.get('sentence','')
    print(f"\n----DEBUG: Sentence Length Check ---")
    print("Sentence: '{sentence}' ({len(sentence)}) chars")
    is_short = len(sentence) <= 50
    print("IS sentence Short? {is_short}")
    return is_short

sentence_length_checker = RunnableLambda(is_sentence_short)

# 6. Branch 1: Elaborate if the sentence is short
elaborate_prompt = ChatPromptTemplate.from_messages([
    ("system","Elaborate on the following sentence using these keywords, adding more details"),
    ("user","Sentence: {sentence}\nKeyword: {keywords}\nElaboration")
])


elaborate_chain = elaborate_prompt | model |StrOutputParser()

#7. Branch 7: Summarize if the sentence is long
summarize_prompt = ChatPromptTemplate.from_messages([
    ("system","Summarize the following sentence concisely, using these keywords to guide the summary"),
    ("user","Sentence: {sentence}\nKeyword: {keywords}\nSummary")
])
summarize_chain = summarize_prompt | model | StrOutputParser()

#8. RunnableBranch: Direct flow based on the condition

conditional_branch = RunnableBranch(
    (sentence_length_checker, elaborate_chain), 
    summarize_chain
)

#----ASsemble the full complex Chain---------------

final_complex_chain = parallel_generation | conditional_branch

print("--- Visualizing the complex Chain as ASCII Graph----") 
final_complex_chain.get_graph().print_ascii()