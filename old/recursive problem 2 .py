import cv2
import numpy as np
import matplotlib.pyplot as plt


def find_e(n,a=0,b=0,start = False):
    m = n+a+b # total flips (n is flips left, a is H, b is T)
    if start:
        global E
        global P
        E = np.ones((m+1,m+1))*np.nan #(x,y) represents (x=total flips so far, y = of those num H)
        P = np.zeros((m+1,m+1)) #at (x,y) whether the strategy makes you proceed or stop (1 if proceed, -1 if stop)
        E[m,:] = np.arange(m+1)*2-m
    if not np.isnan(E[a+b,a]):
        return E[a+b,a]
    Pa = (a+1)/(a+b+2)
    Pb = (b+1)/(a+b+2)
    flip = Pa*find_e(n-1,a+1,b)+Pb*find_e(n-1,a,b+1)
    if a-b>flip:
        E[a+b,a] = a-b
        P[a+b,a] = -1
    else:
        E[a+b,a] = flip
        P[a+b,a] = 1
    return E[a+b,a] 

#"""
find_e(100, start=True)
Pcolor = np.ones(P.shape)*127
Pcolor += (P==1)*128
Pcolor -= (P==-1)*127

Quit = [] #with H heads, how many tails we need to quit -10 if we don't quit
for H in range(100):
    if -1 in list(P[:,H]):
        Quit.append(list(P[:,H]).index(-1)-2*H)
    else:
        Quit.append(0)

plt.plot(Quit)
plt.savefig('quit2.png')

"""Pcolor = cv2.resize(Pcolor, (1000-1000%31,1000-1000%31),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('test2.bmp',Pcolor)

for k in range(10,1000,10):
    print(find_e(k, start=True)/k)
"""
