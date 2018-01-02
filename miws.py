import random
from bokeh.client import push_session
from bokeh.plotting import figure, curdoc
from bokeh.models import BoxAnnotation
from numba import jit
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

class Node:
    def __init__(self, index, weight, adjVec = []):
        self.index = index
        self.weight = weight
        self.adjVec = adjVec
        self.adjNum = 1
        for i in adjVec:
            if i == 1:
                self.adjNum += 1
        self.weightPerNumPlusOne = float(weight)/float(self.adjNum)

    def getAdjNode(self):
        temp = []
        for index,value in enumerate(self.adjVec):
            if value == 1:
                temp.append(index)
        return temp

#####################################################################################

weightList = []
graphList = []
MWIS = []
currentState = []
lastState = []
totalWeight = 0
ranInOut = [0, 1]
infiniteFlag = False

file = open('test1.txt', 'r')      #you can modify testfile here
for i,line in enumerate(file):
    if i == 1:
        for plot in line.split():
            weightList.append( int(plot))
    elif i > 1:
        graphList.append( Node( i-2, weightList[i-2], list( map( int, line.split()))))
        lastState.append(-1)
        currentState.append(random.choice(ranInOut))
file.close()

######################################################################################
# declare figure #  


#p = figure(toolbar_location=None,output_backend="webgl")
p = figure(toolbar_location=None, plot_height=1000, plot_width=1000)
r = p.circle(x=[], y=[], color="skyblue", line_width=4, size=25)
box = BoxAnnotation(top=1.3, bottom=0.5, fill_color='pink', fill_alpha=0.5)
p.add_layout(box)

ds = r.data_source


# count = 1

def inChange(node):
    global currentState, graphList, lastState
    for adjNode in node.getAdjNode():
        if lastState[adjNode] == 1 and node.weightPerNumPlusOne < graphList[adjNode].weightPerNumPlusOne:
            flag = 0
            break
        elif lastState[adjNode] and node.weightPerNumPlusOne == graphList[adjNode].weightPerNumPlusOne:
            if node.index < graphList[adjNode].index:
                flag = 0
                break
            else:
                flag = 1
        else:
            flag = 1
    if flag == 1:
        currentState[node.index] = 1
        #return 1
    elif flag == 0:
        currentState[node.index] = 0
        #return 0

# while currentState !=  stopState:

def compute():
    global currentState, graphList, lastState

    lastState = currentState[:]
    for node in graphList:
    # pool = ProcessPoolExecutor(max_workers=cpu_count())  
    # currentState = list(pool.map(inChange,graphList))
        inChange(node)
        # for adjNode in node.getAdjNode():
        #     if lastState[adjNode] == 1 and node.weightPerNumPlusOne < graphList[adjNode].weightPerNumPlusOne:
        #         flag = 0
        #         break
        #     elif lastState[adjNode] and node.weightPerNumPlusOne == graphList[adjNode].weightPerNumPlusOne:
        #         if node.index > graphList[adjNode].index:
        #             flag = 0
        #             break
        #         else:
        #             flag = 1
        #     else:
        #         flag = 1
        # if flag == 1:
        #     currentState[node.index] = 1
        # elif flag == 0:
        #     currentState[node.index] = 0


    # randomIndex = np.random.randint(0,len(currentState)-1)
    # for adjNode in graphList[randomIndex].getAdjNode():
    #     if currentState[adjNode] == 1 and graphList[randomIndex].weightPerNumPlusOne <= graphList[adjNode].weightPerNumPlusOne:
    #         flag = 0
    #         break
    #     else:
    #         flag = 1
    # if flag == 1:
    #     currentState[randomIndex] = 1
    # elif flag == 0:
    #     currentState[randomIndex] = 0   

    # for node in graphList:
    #     for adjNode in node.getAdjNode():
    #         if currentState[adjNode] == 1 and node.weightPerNumPlusOne <= graphList[adjNode].weightPerNumPlusOne:
    #             flag = 0
    #             break
    #         else:
    #             flag = 1
    #     if flag == 1:
    #         stopState[node.index] = 1
    #     elif flag == 0:
    #         stopState[node.index] = 0
    # if count > len(currentState)*100:
    #     infiniteFlag = True
    #     break
    
    new_data = dict()
    new_data['x'] = [i for i in range(len(currentState))]
    new_data['y'] = currentState
    ds.data = new_data
    
#for i in graphList:
# print(i.index, i.weight , i.adjVec, i.adjNum, i.weightPerNumPlusOne)
#print(currentState)

# for i,choose in enumerate(currentState):
#     if choose == 1:
#         MWIS.append(i)
#         totalWeight += graphList[i].weight
# print(MWIS)
# print(totalWeight)


curdoc().add_periodic_callback(compute, 500)
curdoc().add_root(p)