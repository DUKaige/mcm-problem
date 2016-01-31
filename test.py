import random
def produceMediaDictionary(population,rradio,rtv,rinternet,rnewspaper):
    if rnewspaper > 100:
        rnewspaper = 100
    nradio = int(population*(100- rradio))/100
    ntv = int(population*(100-rtv))/100
    ninternet = int(population*(100-rinternet))/100
    nnewspaper = int(population*(100-rnewspaper))/100
    aradio = range(0,population)
    atv = range(0,population)
    ainterest = range(0,population)
    anewspaper = range(0,population)
    for i in range(0,nradio):
        del aradio[random.randint(0,len(aradio)-1)]
    for i in range(0,ntv):
        del atv[random.randint(0,len(atv)-1)]
    for i in range(0,ninternet):
        del ainterest[random.randint(0,len(ainterest)-1)]
    for i in range(0,nnewspaper):
        del anewspaper[random.randint(0,len(anewspaper)-1)]
    aaradio = []
    aatv = []
    aainterest = []
    aanewspaper = []
    for i in range(0,population):
        if i in aradio:
            aaradio.append(True)
        else:
            aaradio.append(False)
    for i in range(0,population):
        if i in atv:
            aatv.append(True)
        else:
            aatv.append(False)
    for i in range(0,population):
        if i in ainterest:
            aainterest.append(True)
        else:
            aainterest.append(False)
    for i in range(0,population):
        if i in anewspaper:
            aanewspaper.append(True)
        else:
            aanewspaper.append(False)

    for i in range(0,population):
        if aanewspaper[i]:
            if aainterest[i]:
                aatv[i] = False
                aaradio[i] = False
            else:
                if aatv[i]:
                    aaradio[i] = False

        else:
            if aainterest[i]:
                if aatv[i]:
                    aaradio[i] = False
    return (aanewspaper,aaradio,aatv,aainterest)
print produceMediaDictionary(10,98,98,50,80)
#nx.draw_networkx(dg,pos)
#plt.show()
