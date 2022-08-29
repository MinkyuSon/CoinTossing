#https://stackoverflow.com/questions/64394200/scipy-how-to-fit-this-beta-distribution-using-python-scipy-curve-fit

import numpy as np
from scipy.optimize import curve_fit
from scipy.special import gamma as gamma
from matplotlib import pyplot as plt

def betafunc(x,a,b,cst):
    return cst*gamma(a+b) * (x**(a-1)) * ((1-x)**(b-1))  / ( gamma(a)*gamma(b) )


y = np.load('P_100000.npy')
y = y[:(y.shape[0]+1)//2]
x = np.arange(y.shape[0])
x = x/int(x.shape[0])
y = y/np.sqrt(y.shape[0])


popt2,pcov2 = curve_fit(betafunc,x,y,p0=(1.23,1.55,1))

print(popt2)
print(pcov2)

from matplotlib import pyplot as plt
#plt.plot(x,betafunc(x,*popt2))
#plt.plot(x,y)
#plt.savefig('')
