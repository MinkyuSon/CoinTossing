import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.special import gamma as gamma

def find_e_opt(n,a=0,b=0): #Optimized to O(n) data size
    """finds the expected return on optimal play if we have n flips left with aHbT observed.
    Note: To use this to estimate the general game where we start with the knowledge of aHbT, simply substract a-b from the returned value
    """
    m = n+a+b
    global E_old
    global E_new
    global P
    E_old = np.ones((m+1))*np.nan # we store scores of (x,y) for constant x at each stage (x,y) represents (x=total flips so far, y = of those num H)
    E_new = np.ones((m+1))*np.nan
    P = np.zeros((m+1)) #for each num H, mark maximum num T allowed to continue flipping
    E_old = np.arange(m+1)*2-m
    for x in range(m-1,a+b-1,-1):
        first_stop = True
        for y in range(0,x+1):
            Pa = (y+1)/(x+2)
            Pb = (x-y+1)/(x+2)
            flip = Pa*E_old[y+1]+Pb*E_old[y]
            if y-(x-y)>flip:
                E_new[y] = y-(x-y)
            else:
                P[y] = max((x-y)-y, P[y])
                E_new[y] = flip
        E_old = E_new.copy()
        E_new = np.ones((m+1))*np.nan
    return E_old[a]

def betafunc(x,a,b,cst):
    return cst*gamma(a+b) * (x**(a-1)) * ((1-x)**(b-1))  / ( gamma(a)*gamma(b) )

def tolerance(H,n):
    return np.sqrt(n)*betafunc(2*(H+1/2)/n,1.23989379, 1.55704953, 0.34452932) #the 1/2 in H+1/2 was added to allow H=0 to not return 0. The choice of 1/2 was entirely arbitrary.


def find_e_td(n,a=0,b=0): #used estimated tolerance distribution,  tolerance(H) = sqrt(H)*0.48723805*Beta(1.23989379, 1.55704953)(2H/n)
    m = n+a+b
    global E_old
    global E_new
    global P
    E_old = np.ones((m+1))*np.nan # we store scores of (x,y) for constant x at each stage (x,y) represents (x=total flips so far, y = of those num H)
    E_new = np.ones((m+1))*np.nan
    P = np.zeros((m+1)) #for each num H, mark maximum num T allowed to continue flipping
    E_old = np.arange(m+1)*2-m
    for x in range(m-1,a+b-1,-1):
        first_stop = True
        for y in range(0,x+1):
            Pa = (y+1)/(x+2)
            Pb = (x-y+1)/(x+2)
            flip = Pa*E_old[y+1]+Pb*E_old[y]
            if y>m//2:
                P[y] = max((x-y)-y, P[y])
                E_new[y] = flip
            elif (x-y)-y> tolerance(y,n): #if T-H > tolerance
                E_new[y] = y-(x-y)
            else:
                P[y] = max((x-y)-y, P[y])
                E_new[y] = flip
        E_old = E_new.copy()
        E_new = np.ones((m+1))*np.nan
    return E_old[a]

"""
ns = [100,1000,10000,100000]
Ps = []
for n in ns:
    if (n != 100000) and (n != 10000):
        find_e_opt(n)
        Ps.append((2*np.arange(P.shape[0]//2)/int(P.shape[0]),P.copy()[:P.shape[0]//2]/np.sqrt(P.shape[0])))
    else:
        if n==10000:
            P = np.load('P_10000.npy')
        else:
            P = np.load('P_100000.npy')
        Ps.append((2*np.arange(P.shape[0]//2)/int(P.shape[0]),P.copy()[:P.shape[0]//2]/np.sqrt(P.shape[0])))
        
plt.rcParams["figure.figsize"] = (12,4)
fig, axes = plt.subplots(1,4)
fig.suptitle('Tolerance at Different Values of n')
for ax in axes:
    ax.set_xlim(-0.2,1.2)
    ax.set_ylim(0,0.5)
axes[0].set_title('n=100')
axes[0].plot(Ps[0][0],Ps[0][1])
axes[1].set_title('n=1000')
axes[1].plot(Ps[1][0],Ps[1][1])
axes[2].set_title('n=10000')
axes[2].plot(Ps[2][0],Ps[2][1])
axes[3].set_title('n=100000')
axes[3].plot(Ps[3][0],Ps[3][1])
plt.savefig('tolerances.png',bbox_inches='tight')
"""

"""
start=time.time()
n=1000
find_e_opt(n)
np.save('P_{n}.npy'.format(n=n), P)
plt.plot(P)
plt.title('T tolerance for each H at n={n}'.format(n=n))
plt.savefig('P_{n}.png'.format(n=n))
print(time.time()-start)
"""

"""
n=500000
P = np.load('P_500000.npy')
P = (2*np.arange(P.shape[0]//2)/int(P.shape[0]),P.copy()[:P.shape[0]//2]/np.sqrt(P.shape[0]))
plt.rcParams["figure.figsize"] = (12,4)
fig, axes = plt.subplots(1,3)
fig.suptitle('Comparison to Beta Distribution')
for ax in axes:
    ax.set_xlim(-0.2,1.2)
    ax.set_ylim(0,0.5)

axes[0].set_title('n=500000')
axes[0].plot(P[0],P[1])
axes[1].set_title('Beta Distribution')
axes[1].plot(P[0],betafunc(P[0],1.23989379 ,1.55704953 ,0.34452932))
axes[2].set_title('Combined')
axes[2].plot(P[0],P[1])
axes[2].plot(P[0],betafunc(P[0],1.23989379 ,1.55704953 ,0.34452932))
plt.savefig('tolerance1.png',bbox_inches='tight')
"""
