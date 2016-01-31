import numpy
import math
import random
import networkx as nx
total = 1000
internetDelay = 0.08
timeInterval = 0.01
rePostRate = 0.1
explosiveness = 0.3
newspaperDelay = 0.5
totalTime = 4
klink = 15
randlink = 200
radioDens = 10

def negativeExpo(time):
    return math.e**(-2.575*time)

def judgeWithRate(r):
    if random.random()<r:
        return True
    else:
        return False

def gammaFunc(value,rate):
        randomVar = numpy.random.gamma(value*rate, scale=1.0/rate, size=None)
        return randomVar

class Person:
    def __init__(self,info,count,access=False,insystem=False):
        self.info = info
        self.count = count
        self.access = access
        self.repost = False
        self.insystem = insystem

    def calcRepostProb(self,rate,time):
        p = rate
        self.repostrate=p*negativeExpo(time)*explosiveness


class radioMOD:
    def __init__(self,dg,rate):
        self.rate = rate
        self.dg = dg
        self.timeLine = 0
        self.record = []
        self.timerec = []
        edgebox = []
        for i in range(total/50):
            lcstr = 'local-'+str(i)
            self.dg.add_node(lcstr)
            for j in range(total/20):
                index = j+i*50
                edgebox.append((lcstr,index,gammaFunc(newspaperDelay,40)))
        self.dg.add_weighted_edges_from(edgebox)
        self.notchosen = []
        for i in range(50):
            self.notchosen.append(i)
        count = int(total/20*self.rate*explosiveness)
        while count>0:
            randa = random.randint(0,total/20-1)
            while not(randa in self.notchosen):
                randa = random.randint(0,total/20-1)
            self.notchosen.remove(randa)
            count -= 1
        for i in range(20):
            lcstr = 'local-'+str(i)
            for j in range(50):
                index = i*50 + j
                if j in self.notchosen:
                    self.dg.node[index]=Person(False,None)
                else:
                    self.dg.node[index]=Person(False,self.dg.edge[lcstr][index]['weight'],True)


    def update(self):
        self.timeLine += timeInterval
        for i in range(total):
            if self.dg.node[i].info:
                continue
            if self.dg.node[i].access:
                self.dg.node[i].count -= timeInterval
                if self.dg.node[i].count<=0:
                    self.dg.node[i].info=True
                    self.record.append(i)
                    self.timerec.append(self.timeLine)

    def updateWithTime(self,time):
        count = int(time/timeInterval)
        for i in range(count):
            self.update()

    def getResult(self):
        result = {}
        self.updateWithTime(totalTime)
        for i in range(len(self.record)):
            result[self.record[i]] = self.timerec[i]
        for i in range(1000):
            if not (i in result):
                result[i] = -1
        return result


class newspaperMOD:
    def __init__(self,dg,rate):
        self.rate = rate
        self.dg = dg
        self.timeLine = 0
        self.record = []
        self.timerec = []
        edgebox = []
        for i in range(total/50):
            lcstr = 'local-'+str(i)
            self.dg.add_node(lcstr)
            for j in range(total/20):
                index = j+i*50
                edgebox.append((lcstr,index,gammaFunc(newspaperDelay,40)))
        self.dg.add_weighted_edges_from(edgebox)
        self.notchosen = []
        for i in range(50):
            self.notchosen.append(i)
        count = int(total/20*self.rate*explosiveness)
        while count>0:
            randa = random.randint(0,total/20-1)
            while not(randa in self.notchosen):
                randa = random.randint(0,total/20-1)
            self.notchosen.remove(randa)
            count -= 1
        for i in range(20):
            lcstr = 'local-'+str(i)
            for j in range(50):
                index = i*50 + j
                if j in self.notchosen:
                    self.dg.node[index]=Person(False,None)
                else:
                    self.dg.node[index]=Person(False,self.dg.edge[lcstr][index]['weight'],True)


    def update(self):
        self.timeLine += timeInterval
        for i in range(total):
            if self.dg.node[i].info:
                continue
            if self.dg.node[i].access:
                self.dg.node[i].count -= timeInterval
                if self.dg.node[i].count<=0:
                    self.dg.node[i].info=True
                    self.record.append(i)
                    self.timerec.append(self.timeLine)

    def updateWithTime(self,time):
        count = int(time/timeInterval)
        for i in range(count):
            self.update()

    def getResult(self):
        result = {}
        self.updateWithTime(totalTime)
        for i in range(len(self.record)):
            result[self.record[i]] = self.timerec[i]
        for i in range(1000):
            if not (i in result):
                result[i] = -1
        return result

class internetMOD:
    def __init__(self,dg,rate,initialQuan):
        self.dg = self.creatLittleWorldEdges(dg)
        self.rate = rate
        self.timeLine = 0
        insystemCount = int(rate*1000)
        chosen = []
        for i in range(insystemCount):
            randn = random.randint(0,999)
            while randn in chosen:
                randn = random.randint(0,999)
            chosen.append(randn)
        for i in range(1000):
            if i in chosen:
                self.dg.node[i] = Person(False,0,insystem=True)
            else:
                self.dg.node[i] = Person(False,0,insystem=False)
        initialGuys = []
        for i in range(initialQuan):
            randn = random.randint(0,999)
            while not (randn in chosen) or randn in initialGuys:
                randn = random.randint(0,999)
            initialGuys.append(randn)

    def creatLittleWorldEdges(self,dg):
        fullbox = []
        edgebox = []
        for i in range(50):
            fullbox.append(i)
        for reg in range(20):
            for j in range(50):
                index1 = reg*50+j
                chosen = []
                for k in range(klink):
                    randn = random.randint(0,49)
                    while (randn in chosen) or (reg*50+randn==index1):
                        randn = random.randint(0,49)
                    chosen.append(randn)
                for k in range(klink):
                    index2 = reg*50+chosen[k]
                    edgebox.append((index1,index2))
        dg.add_edges_from(edgebox)
        edgebox = []
        for i in range(randlink):
            a = random.randint(0,999)
            b = random.randint(0,999)
            areg = a/50
            breg = b/50
            while a==b or areg==breg or ((a,b) in edgebox):
                a = random.randint(0,999)
                b = random.randint(0,999)
                areg = a/50
                breg = b/50
            edgebox.append((a,b))
        dg.add_edges_from(edgebox)
        return dg


class Crowd:
    def __init__(self,newspaperRate,radioRate,TVRate,internetRate):
        self.newspaperGuy = newspaperRate*total
        self.gadioGuy = radioRate*total
        self.TVGuy = TVRate*total
        self.internetGuy = internetRate*total
        self.dg = self.creatSmallWorld(randlink)

    def creatSmallWorld(self,randlink):
        dg = nx.DiGraph()
        node = []
        for i in range(1000):
            node.append(i)
        dg.add_nodes_from(node)
        edgebox = []
        fullbox = []

        return dg

myCrowd = Crowd(0,0,0,0)
dg = myCrowd.dg
myInter = internetMOD(dg,0.5,20)
print myInter.dg.edge


def produceMediaDictionary(population,rradio,rtv,rinternet,rnewspaper):
    nradio = int(population*(1- rradio))
    ntv = int(population*(1-rtv))
    ninternet = int(population*(1-rinternet))
    nnewspaper = int(population*(1-rnewspaper))
    aradio = range(0,population)
    atv = range(0,population)
    ainterest = range(0,population)
    atv = range(0,population)
    for i in range(0,nradio):

