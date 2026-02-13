from langchain_core.runnables import RunnableLambda, RunnableSequence

runnable1 = RunnableLambda(lambda x: x + 5)
runnable2 = RunnableLambda(lambda x: x * 2)


#Demo 1 Runnable using RunnableSequence
# sequence1 = RunnableSequence(
#     first=runnable1,
#     # middle=[],
#     last=runnable2
# )

# result  = sequence1.invoke(5)
# print(result)


#Demo 2 - Runnable using Pipe()
# seq_runnables =runnable1.pipe(runnable2)
# result  = seq_runnables.invoke(4)
# print(result)

#demo 3 Runnable using | sign   LCEL (Langchain Expression Language)
seq_runnables = runnable1 | runnable2
result = seq_runnables.invoke(3)
print(result)