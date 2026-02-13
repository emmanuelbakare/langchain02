from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda input: str(input).upper())
runnable2 = RunnableLambda(lambda input: str(input).lower())

#compose the Runnable Paralles as dictionary
#run the prompt value with runnable1 and store it under dictionary key "uppercase"....
paralle_1 = RunnableParallel({
    "uppercase": runnable1,
    "lowercase": runnable2
})

#compose the Runnable paralle as parameters
paralle_2 = RunnableParallel(
    upper = runnable1,
    lower =  runnable2
)

# result = paralle_1.invoke("Construction Worker")
result = paralle_2.invoke("Construction Worker")
print(result)


#LCEL 

paralle_3 = paralle_2 | (lambda input: input['upper']+ " -- "+ input['lower'])

result = paralle_3.invoke("WorkForce")
print(result)


#One of your LCEL pip must have a runnable if not it will not work
#paralle_4 will not work because there is no runnable 
# paralle_4 = {'upper':'WORKFORCE', 'lower':'workforce'} |  (lambda input: input['upper']+ " -- "+ input['lower'])

#ensure one of the pip is a runnable
# paralle_5 = {'upper':'WORKFORCE', 'lower':'workforce'} | RunnableLambda(lambda input: input['upper']+ " -- "+ input['lower'])  

# result = paralle_5.invoke("TEstER")
# print(result)