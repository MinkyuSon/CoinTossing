import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

def find_e_softmax(n,a=0,b=0):
    m = n+a+b
    global E
    global P
    E = np.ones((m+1,m+1))*np.nan #(x,y) represents (x=total flips so far, y = of those num H)
    E[m,:] = np.arange(m+1)*2-m
    for x in range(m-1,-1,-1):
        for y in range(0,x+1):
            Pa = (y+1)/(x+2)
            Pb = (x-y+1)/(x+2)
            flip = Pa*E[x+1,y+1]+Pb*E[x+1,y]
            E[x,y] = np.log(np.exp(flip)+np.exp((a-b)))
    return E[a+b,a]

def find_e(n,a=0,b=0):
    m = n+a+b
    global E
    global P
    E = np.ones((m+1,m+1))*np.nan #(x,y) represents (x=total flips so far, y = of those num H)
    P = np.zeros((m+1,m+1)) #at (x,y) whether the strategy makes you proceed or stop (1 if proceed, -1 if stop)
    E[m,:] = np.arange(m+1)*2-m
    for x in range(m-1,-1,-1):
        for y in range(0,x+1):
            Pa = (y+1)/(x+2)
            Pb = (x-y+1)/(x+2)
            flip = Pa*E[x+1,y+1]+Pb*E[x+1,y]
            if y-(x-y)>flip:
                E[x,y] = y-(x-y)
                P[x,y] = -1
            else:
                E[x,y] = flip
                P[x,y] = 1
    return E[a+b,a]

f = lambda n,m:((n-1)/2-m)*(m+1)/(2*m+3)

"""
n=1000
find_e(n)
np.savetxt("E2.csv", E/n, delimiter=",")

ev = []
for n in range(1,1000):
    ev.append(find_e(n,1)/n)
"""
"""
diff = [ev[k+1]-ev[k] for k in range(0,len(ev)-1)]
plt.clf()
plt.plot([1/x for x in diff])
plt.savefig('inversediff.png')

"""


n=1000
find_e(n)
Pcolor = np.ones(P.shape)*127
Pcolor += (P==1)*128
Pcolor -= (P==-1)*127

Quit = [] #with H heads, how many tails we need to quit -10 if we don't quit
for H in range(n+1):
    if -1 in list(P[:,H]):
        Quit.append(list(P[:,H]).index(-1)-2*H)
    else:
        Quit.append(0)

plt.plot(Quit)
plt.plot([np.sqrt(n)/3*beta.pdf(x/n*2, 1.23, 1.55) for x in range(1,n//2)])
plt.savefig('test.png')
