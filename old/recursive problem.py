import numpy as np

def find_e(E, n,a=0,b=0):
    if not np.isnan(E[n,a,b]):
        return E[n,a,b]
    Pa = (a+1)/(a+b+2)
    Pb = (b+1)/(a+b+2)
    flip = Pa*find_e(E,n-1,a+1,b)+Pb*find_e(E,n-1,a,b+1)
    ans = max(flip, a-b)
    E[n,a,b] = ans
    return ans

dim = 500

E = np.ones((dim,dim,dim))*np.nan
t = np.arange(dim).reshape((1,dim))
E[0,:,:] = -np.tile(t,(dim,1)) + np.tile(t.T,(1,dim))
