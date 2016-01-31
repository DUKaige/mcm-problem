import networkx as nx
#import matplotlib.pyplot as plt
import random
import numpy
import math
#import multiprocessing
print 'note: 25000-30000'
n = 1000        #Population Count
m = 30000      #Relationship Count
time = 0.08
interval = 0.01
repostRate = 10
explosiveness = 0.5
totalTime = 2

def custumInt(fl):
    if fl-int(fl)<0.5:
        return int(fl)
    else:
        return int(fl)+1

def negativeExpo(time):
    return math.e**(-2.575*time)

class Person:
    def __init__(self,info,count,spreadCount=0,spreading=False,repost=False):
        self.info = info
        self.count = count
        self.access = False
        self.repost = False
        self.repostrate = repostRate*1.0/100*explosiveness
        self.spreading = spreading
        self.spreadCount = spreadCount
        self.reposted = False

    def calcPost(self,timeline):
        self.repost = self.rePostJudge(repostRate,timeline)

    def rePostJudge(self,rate,timeline):
        p = 1.0 * rate / 100
        self.repostrate=p*negativeExpo(timeline)*explosiveness
        #print self.repostrate
        #print self.repostrate
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
        self.i = []


    def initwithMostSocial(self):
        maxcount = 0
        maxindex = 0
        for n in self.dg:
            if len(self.dg[n])>maxcount:
                maxcount = len(self.dg[n])
                maxindex = n
        self.FirstGuy = maxindex
        self.dg.node[self.FirstGuy] = Person(True,0,time,True,True)
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
        icount = 0
        for n in self.dg:
            if self.dg.node[n].info == True and self.dg.node[n].repost == True:
                nodes = self.dg[n]
                nodesCount = len(nodes)
                repostCount = custumInt(self.dg.node[n].repostrate*nodesCount)
                #print repostCount
                repostIndexBox = []
                for i in range(repostCount):
                    randn = random.randint(0,nodesCount-1)
                    while randn in repostIndexBox:
                        randn = random.randint(0,nodesCount-1)
                    repostIndexBox.append(randn)
                index = 0
                box1 = []
                if not self.dg.node[n].reposted:
                    self.dg.node[n].reposted = True
                    for child in nodes:
                        if self.dg.node[child].info == True:
                            continue
                        else:
                            if self.dg.node[child].access == False:
                                self.dg.node[child].count = self.time
                                self.dg.node[child].access = True
                            if index in repostIndexBox:
                                self.dg.node[child].repost = True
                        index += 1
                spreading = False
                for child in nodes:
                    if self.dg.node[child].access == True and self.dg.node[child].info == False:
                        spreading = True
                        break
                self.dg.node[n].spreading = spreading
                if spreading:
                    icount += 1
            else:
                if self.dg.node[n].access == True and self.dg.node[n].info == False and self.dg.node[n].count<0:
                    self.dg.node[n].info = True

                    self.dg.node[n].rePostJudge(repostRate,self.timeLine)
                    self.record.append((n,self.timeLine,self.dg.node[n].repost,self.dg.node[n].repostrate))
                    #self.nodecolor[n-1]=((self.timeLine/totalTime)**(1.0/3),(self.timeLine/totalTime)**(1.0/4),0.5+0.5*(self.timeLine/totalTime)**(1.0/5))
                    #self.linkrecord.append(len(self.dg[n]))
                elif self.dg.node[n].access == True and self.dg.node[n].count>0:
                    self.dg.node[n].count -= interval
        self.i.append(icount)
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
mbox = []
'''
while m<30000:
    mbox.append(m)
    avg = 0
    for i in range(100):
        myCrowd = Crowd(n,m,time)
        myCrowd.updateWithTime(totalTime)
        avg += len(myCrowd.record)
    avg /= 100
    print avg,m
    databox.append(avg)
    m += 10

print databox
print mbox
'''
myCrowd = Crowd(n,m,time)
myCrowd.updateWithTime(totalTime)
print len(myCrowd.record)
print myCrowd.i

#nx.draw_networkx(dg,arrows=False,node_color=myCrowd.nodecolor,with_labels=False)
#plt.show()