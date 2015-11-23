#!/usr/bin/env python3

from numpy import *
from matplotlib import *
from threading import Thread
import time
import sys

#define initial Information

#days infected
k = 20
#infected spread rate
tau = .2
#vaccination rate
nu = .1
#gridsize
gridsize = 10
#total number of threads
total = 100

#get parameters if they exist
if len(sys.argv) > 1:
    for i in range(0,len(sys.argv)):
        if sys.argv[i] == "-tau":
            tau = float(sys.argv[i+1])
        if sys.argv[i] == "-nu":
            nu = float(sys.argv[i+1])
        if sys.argv[i] == "-grid":
            gridsize = int(sys.argv[i+1])
        if sys.argv[i] == "-threads":
            total = int(sys.argv[i+1])
        if sys.argv[i] == "-k":
            k = int(sys.argv[i+1])

class simulate(Thread):
    def __init__(self,k,tau,nu,gridsize):
        Thread.__init__(self)
        self.k = k
        self.tau = tau
        self.nu = nu
        self.gridsize = gridsize
        self.A = []
        self.Z = []
        self.I = []
        self.totinfected = 0
        self.totvaccined = 0
    
    def run(self):
        pop = [[0 for x in range(gridsize)] for x in range(gridsize)]
        
        #for displaying
        def display():
            rowstring = ""
            for i in range(0,gridsize):
                for j in range(0,gridsize):
                    rowstring += str(pop[i][j]) + "  "
                print(rowstring)
                rowstring = ""

        #check if finished with main loop and update the
        #lists
        def check():
            golonger = 0
            tot_i = 0
            tot_a = 0
            tot_z = 0
            for i in range(0,gridsize):
                for j in range(0,gridsize):
                    if pop[i][j] in range(1,k) or pop[i][j] == 'i':
                        golonger = 1
                        tot_i += 1
                    if pop[i][j] == 'Z':
                        tot_z += 1
                    if pop[i][j] == 'A':
                        tot_a += 1
            self.A.append(tot_a)
            self.Z.append(tot_z)
            self.I.append(tot_i)
            return golonger

        #function to run through a new day and see if anybody new gets infected
        #i.e. infecting people that are susceptable and increasing days infected
        def newday():
            for i in range(0,gridsize):
                for j in range(0,gridsize):
                    if pop[i][j] == 'i':
                        self.totinfected += 1
                        pop[i][j] = 1
                        infect(i,j)
                    elif pop[i][j] in range(1,k):
                        if pop[i][j] == k-1:
                            pop[i][j] = 'Z'
                        else:
                            pop[i][j] += 1
                            infect(i,j)
            #change all I into i
            #this is from the infect call that makes them I
            for i in range(0,gridsize):
                for j in range(0,gridsize):
                    if pop[i][j] == 'I':
                        pop[i][j] = 'i'

        #this looks to see who can be infected from the original infected
        #they are put as I instead of i so that they don't infect
        #right after being infected (i.e. that same day)
        def infect(i,j):
            #check above it
            if(i - 1) >= 0 and pop[i-1][j] == 0:
                inf = numpy.random.rand()
                if inf <= self.tau:
                    pop[i-1][j] = 'I'
            if (i + 1) < gridsize and pop[i+1][j] == 0:
                if numpy.random.rand() <= self.tau:
                    pop[i+1][j] = 'I'
            if (j + 1) < gridsize and pop[i][j+1] == 0:
                if numpy.random.rand() <= self.tau:
                    pop[i][j+1] = 'I'
            if (j - 1) >= 0 and pop[i][j-1] == 0:
                if numpy.random.rand() <= self.tau:
                    pop[i][j-1] = 'I'

        #do vaccination check
        #checks if they are infected or recovered, if not it tries to vaccine
        #the nu rate is the percentage of success
        #.1 = 10%... .2 = 20% ... etc
        def vaccine():
            for r in range(0,gridsize):
                for c in range(0,gridsize):
                    #see if they can vaccinate
                    if pop[r][c] == 0:
                        if numpy.random.rand() <= self.nu and pop[r][c] == 0:
                            pop[r][c] = 'A'
        #Run back to the main Run function
        init_r = numpy.random.randint(0,gridsize)
        init_c = numpy.random.randint(0,gridsize)
        
        #infect first person
        pop[init_r][init_c] = 'i'
        
        while check() == 1:
            newday()
            vaccine()


tl = [] #thread list
totsize = 0 #top amount of days

#create all the threads
for i in range(0,total):
    tl.append(simulate(k,tau,nu,gridsize))
    tl[i].start()

#make sure they all returned
#and get their sizes
for i in range(0,total):
    tl[i].join()
    if size(tl[i].A) > totsize:
        totsize = size(tl[i].A)

#make them all the same size
for i in range(0,total):
    print("thread #" + str(i) + " Facts:\n")
    print("Total Infected: " + str(tl[i].totinfected))
    print("List of Vaccinated:")
    print(tl[i].A)
    print("List of Healed:")
    print(tl[i].Z)
    print("List of Infected:")
    print(tl[i].I)
    print("\n\n")
    s = size(tl[i].A)
    #if its smaller than max days, make it right size
    if s < totsize:
        for x in range(s,totsize):
            tl[i].A.append(tl[i].A[s-1])
            tl[i].Z.append(tl[i].Z[s-1])
            tl[i].I.append(0)

#the lists to hold averages
Av_A = []
Av_Z = []
Av_I = []

#now average out everything
for i in range(0,totsize):
    av_a = 0
    av_z = 0
    av_i = 0
    #add all values for each of the threads
    for x in range(0,total):
        av_a += tl[x].A[i]
        av_z += tl[x].Z[i]
        av_i += tl[x].I[i]
    #average them and stick average into list
    Av_A.append(av_a/total)
    Av_Z.append(av_z/total)
    Av_I.append(av_i/total)

#print them out
import matplotlib.pyplot as plt
days = [x for x in range(size(Av_A))]
plt.plot(days,Av_A,'go',label="vaccine")
plt.plot(days,Av_Z,label="healed",linestyle='--')
plt.plot(days,Av_I,label="infected",color = 'red')

plt.legend(loc=2)
plt.show()
