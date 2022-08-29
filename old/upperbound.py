import numpy as np


def prod(xs):
    P = 1
    for x in xs:
        P *= x
    return P

fact = lambda n:prod(list(range(1,n+1))) if n>0 else 1

def C(n,k):
    if (n<0) or (k<0) or (k>n):
        return 0
    k = max(k,n-k)
    P = 1
    for i in range(1,n-k+1):
        P *= (k+i)/i
    return P


def N(n,k):
#    m = int(np.sqrt(n))
    m=n//2-int(np.sqrt(n))
    Sum = 0
    for i in range(m//2,m+1):
        Sum += C(m,i)*C(n-m,k-i)
    return Sum

def UB(n):
    ev = 0
    for m in range((n+1)//2,n):
        ev += (2*m-n)*N(n,m)/C(n,m)/(n+1)
    return ev
