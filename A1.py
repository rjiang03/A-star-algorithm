import numpy as np
from copy import deepcopy
import heapq


def heristic(list):# heristic function, check the number of the pancake on the wrong position
    length = len(list)
    h = 0

    for i in range(length - 1):
        if (np.abs(list[i] - list[i + 1])) > 1:
            h = h + 1

    return h

class Node(list):
    def __init__(self, list):
        #insert a larger number in the head
        list.insert(0, max(list)+1)
        #record the list
        self.list = list
        # initialize the cost
        self.cost = 0
        self.h = heristic(self.list)
        # the total cost
        self.g = self.cost + self.h
        # initialize its parent
        self.parent = 0

def flip(Node, num):
    Nc = deepcopy(Node)
    length = len(Nc.list)
    #test error
    if num > length-1:
        return
    if num <= 1:
        return

    #flip every one after number
    for i in range((length-num+1) // 2):
        temp = Nc.list[num-1+i]
        Nc.list[num-1+i] = Nc.list[length-1-i]
        Nc.list[length-1-i] = temp

    #updata cost
    Nc.cost = Nc.cost + 1
    Nc.h = heristic(Nc.list)
    Nc.g = Nc.h + Nc.cost
    Nc.parent = Node

    return Nc

class PriorityQueue(object):
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, Node, priority):
        i = 0
        #check whether there is node with same list has larger total cost
        while i < len(self._queue):
            if Node.list == self._queue[i][2].list:
                if Node.g < self._queue[i][2].g:
                    del self._queue[i]
                    #self._index -= 1
                    break
            i = i + 1
        heapq.heappush(self._queue, (priority, self._index, Node))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

def printf(Node):
    #print from the very top
    if Node.parent != 0:
        printf(Node.parent)

    print(Node.list[1:len(Node.list)])

def Astar(Node):
    FRONTIER = PriorityQueue()
    VISITED = [Node]

    if Node.h == 0:
        print(Node.list)
        return Node

    while True:
        #choose the last one from visited to find its child
        for i in range(len(VISITED[-1].list)-2):
            temp = deepcopy(flip(VISITED[-1], i + 2))
            m = 0
            #check if it has been visited before
            for j in range(len(VISITED)):
                if VISITED[j].list == temp.list:
                    m = m + 1
            #if it has not been visited before
            if(m == 0):
                FRONTIER.push(temp, temp.g)

        #temp is the one with smallest g
        temp2 = FRONTIER.pop()

        VISITED.append(temp2)

        #if it is the goal
        if temp2.h == 0:
            printf(temp2)
            return temp2
        else:
            del temp2


list = []
print("Please input numbers from bottom to top\nInput end to end input")
while True:
    a = input()
    if a == 'end':
        break
    else:
        list.append(int(a))

a = Node(list)

Astar(a)