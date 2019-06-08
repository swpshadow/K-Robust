import json
import os
import statistics
import math
from operator import attrgetter

class Agent:
    tasks = []
    cost = int
    agentNum = int
    taskLength = int
    costPerTask = int

    def __init__(self):
        self.cost = 0
        self.agentNum = 0
        self.taskLength = 0
        self.tasks = []
        self.costPerTask = 0

    def addToList(self, i):
        for num in i:
            self.tasks.append(num)
        self.taskLength =  self.tasks.__len__()

    def updateLength(self):
        self.taskLength = self.tasks.__len__()

    def getCostPerTask(self):
        if(self.taskLength > 0 ):
            return self.cost / self.tasks.__len__()
        else:
            return 10000000
    def updateCostPerTask(self):
        if self.tasks:
            self.costPerTask = self.cost / self.tasks.__len__()
        else:
            self.costPerTask = 1000000

#end class Agent

#Marginally better cost than neededTaskAlg (may be statistically insignificant)
#but uses more agents.
#Way lower cost compared to greedy.
#Algorithm selects the agent with the lowest cost per task. Only takes in
#to account tasks that are not k robust already.
def adaptiveGreedyAlg(agents,numTasks, k):
    G = []
    listOfTasks = [0] * numTasks

    while isNotKRobust(G, numTasks, k):
        x = min(agents, key = attrgetter('costPerTask') )
        G.append(x)
        agents.remove(x)
        for t in x.tasks:
            listOfTasks[t] += 1
            if listOfTasks[t] > k:
                for a in agents:
                    if t in a.tasks:
                        a.tasks.remove(t)
                        a.updateCostPerTask()
    return G

#is a modification of neededTaskAlg that only takes in to account
#the tasks not yet k robust when calculating minimum cost per task.
#performs insanely well. like, damn.
def multiNeededTaskAlg(agents, numTasks, k):
    G = []
    listOfTasks = [0] * numTasks
    lowestTask = 0
    while isNotKRobust(G, numTasks, k):
        s = []
        lowestTask = listOfTasks.index(min(listOfTasks)) ##finds least covered task
        for a in agents: #makes a list of agents 's' that contain lowestTask
            if lowestTask in a.tasks:
                s.append(a)
        x = min(s, key = attrgetter('costPerTask')) #gets lowest cost over number of tasks agent from 's'
        agents.remove(x)
        G.append(x)
        for t in x.tasks: #updates list of covered tasks
            listOfTasks[t] += 1
            if listOfTasks[t] > k: #removes tasks already k robust from calculations
                for a in agents:
                    if t in a.tasks:
                        a.tasks.remove(t)
                        a.updateCostPerTask()
    return G


#finds the task with the lowest number of agents doing that task then selects an agent with the
#lowest cost per task to do that
def neededTaskAlg(agents, numTasks, k):
    G = []
    listOfTasks = [0] * numTasks
    lowestTask = 0
    while isNotKRobust(G, numTasks, k):
        s = []
        lowestTask = listOfTasks.index(min(listOfTasks)) ##finds least covered task
        for a in agents: #makes a list of agents 's' that contain lowestTask
            if lowestTask in a.tasks:
                s.append(a)
        x = min(s, key = attrgetter('costPerTask')) #gets lowest cost over number of tasks agent from 's'
        agents.remove(x)
        G.append(x)
        for t in x.tasks: #updates list of covered tasks
            listOfTasks[t] += 1
    return G

#awful algorithm. please ignore.
# def underAverageAlg(agents, numTasks, k):
#     G = []
#     avg = 0
#
#     while  isNotKRobust(G, numTasks, k) and agents:
#         avg = 0
#         for ag in agents:
#             avg += ag.costPerTask
#         avg = avg/agents.__len__()
#         c = []
#         for a in agents:
#             if(a.getCostPerTask() < avg):
#                 c.append(a)
#         avg = 0
#         uc = []
#         for ag in c:
#             avg += ag.costPerTask
#         avg = avg/c.__len__()
#         uc = []
#         for a in agents:
#             if(a.getCostPerTask() < avg):
#                 uc.append(a)
#         while isNotKRobust(G, numTasks, k) and uc:#and agents below avg cost per task
#             x = max(uc, key=attrgetter('taskLength'))
#             #print(x.tasks)
#             agents.remove(x)
#             uc.remove(x)
#             G.append(x)
#     return G

#pretty damn good for being so simple

def greedyAlg(agents, numTasks, k):
    G = []
    while isNotKRobust(G, numTasks, k):
        x = min(agents, key = attrgetter('costPerTask') )
        G.append(x)
        agents.remove(x)
    return G

#determines if set G is k robust in linear time.
def isNotKRobust(G, numTasks, k):
    if G:
        listOfTasks = [0] * numTasks
        for ag in G:
            for t in ag.tasks:
                listOfTasks[t] +=1
        x = min(listOfTasks)
        #print(listOfTasks)
        return (x - 1) < k
    else:
        return not G

#################################################################################################
#begin main

totalX = 0
lengthX = 0
total = 0
length = 0
count = 0

size = '30Agents'


for filename in os.listdir('.\\' + size):
    data = []
    if filename.endswith('.json'):
        try:
            with open(os.path.join('.\\' + size + '\\', filename)) as f:
                data = json.load(f)
        except IOError:
            print("error opening: ", filename)

        numTasks = data[1]
        numAgents = data[0]
        k = 4
        agents = []
        for i in range(numAgents):
            x = Agent()
            x.cost = data[2][i]
            x.addToList(data[3][i])
            x.updateCostPerTask()
            agents.append(x)

        G = []
        G = multiNeededTaskAlg(agents, numTasks, k)

        totalCost = 0
        for a in G:
            totalCost += a.cost
        length += G.__len__()
        print("the cost of run ", count, ": ",totalCost, "\n", G.__len__() )
        total += totalCost

        # X = []
        # X = multiNeededTaskAlg(agents, numTasks, k)
        # totalCostX = 0
        # for x in X:
        #     totalCostX += x.cost
        # totalX += totalCostX
        # lengthX += X.__len__()

        count +=1

print("the total average G: ",total/count)
print("the average length G: ", length/count)
