import numpy as np

def C(n,k):
    if (n<0) or (k<0) or (k>n):
        return 0
    k = max(k,n-k)
    P = 1
    for i in range(1,n-k+1):
        P *= (k+i)/i
    return P


def path(m,n,k, data=False):
    """number of path on m by n grid from (0,0) to (m,n) staying on or below the line y=x+k"""
    assert k>=0
    grid = np.zeros((m+1,n+1))
    grid[0,:]=1
    grid[:k+1,0]=1
    for U in range(1,m+1):
        for R in range(1,n+1):
            if U>R+k:
                grid[U,R]=0
            else:
                grid[U,R] = grid[U-1,R]+grid[U,R-1]
    if data:
        return grid
    return grid[-1,-1]


def general_catalan(m,n,k):
    return C(m+n,m)-C(m+n,m-k-1)

def UB(n):
    ev = 0
    for m in range((n+1)//2,n+1):
        ev += (2*m-n)*(general_catalan(n-m,m,int(np.sqrt(n))))/C(n,m)/(n+1)
    return ev
