import numpy as np
from scipy.stats import beta

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


def fact(n):
    if n==0:
        return 1
    return n*fact(n-1)

prod = lambda x:x[0]*prod(x[1:]) if len(x)>0 else 1

def C(n,k):
    k = max(k,n-k)
    return prod(range(k+1,n+1))/fact(n-k)

def E1(n,a,b):
    return (a-b)*(n-a-b)/(a+b+2)

def E2(n,a,b):
    Sum = 0
    for k in range(a,n-b+1):
        Sum += C(k,a)*C(n-k,b)
    return Sum/C(n+2,a+b+2)

def tolerance_beta(n,H):
    return int(np.sqrt(n)/3*beta.pdf(H/n*2, 1.23, 1.55))+1

def tolerance(n):
    find_e(n)
    Quit = [] #with H heads, how many tails we need to quit -10 if we don't quit
    for H in range(n+1):
        if -1 in list(P[:,H]):
            Quit.append(list(P[:,H]).index(-1)-2*H)
        else:
            Quit.append(0)
    return Quit

def num_path(n,k,tolerance):
    """number of path from (H,T) = (0,0) to (k,n-k) where we stop if (x,y) s.t. y-x>sqrt(n)"""
    To = tolerance
    path_count = np.zeros((k,n-k))
    path_count[:,0] = 1
    path_count[0,min(n-k-1,To[0]+1)] = 1
    for H in range(k):
        for T in range(n-k):
            if T-H>To[H]:
                path_count[H,T]=0
            else:
                if H-1>-1:
                    path_count[H,T] += path_count[H-1,T]
                if T-1>-1:
                    path_count[H,T] += path_count[H,T-1]
    return path_count[-1,-1]




def E3(n):
    To = tolerance(n)
    ev = 0
    for m in range((n+1)//2,n):
        ev += (2*m-n)*num_path(n,m, To)/C(n,m)/(n+1)
    return ev
