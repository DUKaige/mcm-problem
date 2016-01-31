import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy
n = 20        #Population Count
m = 150       #Relationship Count
time = 0.08

dg = nx.DiGraph()
dg.add_nodes_from([1,2,3])
dg.add_weighted_edges_from([(1,2,1),(1,3,0.5)])
dg.add_node('a')
a= 1
b = a+0.1
print b

def custumInt(fl):
    if fl-int(fl)<0.5:
        return int(fl)
    else:
        return int(fl)+1

a = {1:1,2:3,4:5}
print (3 in a)


#nx.draw_networkx(dg,pos)
#plt.show()
