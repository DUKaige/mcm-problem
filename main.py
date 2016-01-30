import networkx as nx
#import matplotlib.pyplot as plt
import random
import numpy
import math
#import multiprocessing
print 'note: 3-3.99'
n = 1000        #Population Count
m = 30000      #Relationship Count
time = 0.08
interval = 0.01
repostRate = 10
explosiveness = 0.5
totalTime = 3

def negativeExpo(time):
    return math.e**(-2.575*time)

class Person:
    def __init__(self,info,count):
        self.info = info
        self.count = count
        self.access = count
        self.repost = False
        self.repostrate = 1

    def calcPost(self,time):
        self.repost = self.rePostJudge(repostRate,time)

    def rePostJudge(self,rate,time):
        p = 1.0 * rate / 100
        self.repostrate=p*negativeExpo(time)*explosiveness
        if random.random()<self.repostrate:
            return True
        else:
            return False

class Crowd:
    def __init__(self,n,m,time):
        self.dg,self.edgebox = self.creatRelationshipMap(n,m)
        self.nodecolor = []
        self.fontcolor = []
        for i in self.dg:
            self.dg.node[i] = Person(False,0)
            self.nodecolor.append((1,0,0))
        #self.linkrecord = [self.initwithMostSocial()]
        self.initwithMostSocial()
        #self.initwithOne(n)
        self.time = time
        self.record = [(self.FirstGuy,0)]
        self.nodecolor[self.FirstGuy-1]=(0,0,0.5)
        self.timeLine = 0


    def initwithMostSocial(self):
        maxcount = 0
        maxindex = 0
        for n in self.dg:
            if len(self.dg[n])>maxcount:
                maxcount = len(self.dg[n])
                maxindex = n
        self.FirstGuy = maxindex
        self.dg.node[self.FirstGuy] = Person(True,0)
        self.dg.node[self.FirstGuy].repost = True
        return maxcount

    def initwithOne(self,n):
        self.FirstGuy = 1
        self.dg.node[self.FirstGuy] = Person(True,0)
        self.dg.node[self.FirstGuy].repost = True
    def getMap(self):
        return self.dg


    def creatRelationshipMap(self,n,m):
        dg = nx.DiGraph()
        nbox = []
        for i in range(n):
            nbox.append(i+1)
        edgebox = []
        dg.add_nodes_from(nbox)
        for i in range(n):
            box = []
            for j in range(int(m/n)):
                randn = random.randint(0,n-1)
                while randn==i or (randn in box):
                    randn = random.randint(0,n-1)
                edgebox.append((i,randn))
                box.append(randn)
            '''
            a = random.randint(1,n)
            b = random.randint(1,n)
            while ((a,b) in edgebox) or a==b:
                a = random.randint(1,n)
                b = random.randint(1,n)
            edgebox.append((a,b))
            '''
        dg.add_edges_from(edgebox)
        return dg,edgebox

    def gammaFunc(self):
        randomVar = numpy.random.gamma(self.time*100, scale=1.0/100, size=None)
        return randomVar

    def update(self):
        self.timeLine += interval
        #print self.timeLine
        for n in self.dg:
            if self.dg.node[n].info == True:
                nodes = self.dg[n]
                nodesCount = len(nodes)
                repostCount = int(self.dg.node[n].repostrate*nodesCount)
                repostIndexBox = []
                for i in range(repostCount):
                    randn = random.randint(0,nodesCount-1)
                    while randn in repostIndexBox:
                        randn = random.randint(0,nodesCount-1)
                    repostIndexBox.append(randn)
                index = 0
                for child in nodes:
                    if self.dg.node[child].info == True:
                        continue
                    elif index in repostIndexBox:
                        if self.dg.node[child].access == False:
                            self.dg.node[child].count = self.time
                            self.dg.node[child].access = True
                    index += 1
            else:
                if self.dg.node[n].access == True and self.dg.node[n].count <= 0:
                    self.dg.node[n].info = True
                    self.dg.node[n].calcPost(self.timeLine)
                    self.record.append((n,self.timeLine,self.dg.node[n].repost,self.dg.node[n].repostrate))
                    #self.nodecolor[n-1]=((self.timeLine/totalTime)**(1.0/3),(self.timeLine/totalTime)**(1.0/4),0.5+0.5*(self.timeLine/totalTime)**(1.0/5))
                    #self.linkrecord.append(len(self.dg[n]))
                elif self.dg.node[n].access == True:
                    self.dg.node[n].count -= interval
        return

    def updateWithTime(self,days):
        ct = int(days/interval)
        for i in range(ct):
            self.update()

avgbox = []
totalTimebox = []
'''
while totalTime<=4:
    totalTimebox.append(totalTime)
    total = 0
    for i in range(100):
        myCrowd = Crowd(n,m,time)
        myCrowd.updateWithTime(totalTime)
        total += len(myCrowd.record)
    avg = int(total/100)
    avgbox.append(avg)
    totalTime += 0.01
print totalTimebox
print avgbox
'''

databox = []
timebox = []
while totalTime<4:
    timebox.append(totalTime)
    avg = 0
    for i in range(100):
        myCrowd = Crowd(n,m,time)
        myCrowd.updateWithTime(totalTime)
        avg += len(myCrowd.record)
    avg /= 100
    print avg,totalTime
    databox.append(avg)
    totalTime += interval

print databox
print totalTime


#nx.draw_networkx(dg,arrows=False,node_color=myCrowd.nodecolor,with_labels=False)
#plt.show()