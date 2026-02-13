
from langchain_core.runnables import RunnableLambda

#lambda function
# addten = lambda x: x + 10
# print(addten(5))

#Runnable to a lambda function
# addten =RunnableLambda(lambda x: x + 10)
# result = addten.invoke(3)
# print(result)

#batch method on runnable
# result2 = addten.batch([10,3,23])
# print(result2)


#runnable on Function
# the function adds 2 values of a dictionary

def addTwoNum(inputs):
    return inputs['x'] + inputs['y'] 

runnable2 = RunnableLambda(addTwoNum)

result  = runnable2.invoke({"x":12, "y":5})
print(result)