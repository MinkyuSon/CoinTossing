import numpy as np
import random
import matplotlib.pyplot as plt
import time
import h5py

P_100 = np.load('P_100.npy')
P_1000 = np.load('P_1000.npy')
P_10000 = np.load('P_10000.npy')
Ps = [P_100, P_1000, P_10000]
ns = [100,1000,10000]
epoch_count=10**7
sum_scores_ns = h5py.File('0H1T_simulation_data.hdf5','a')

for k in range(3):
    start = time.time()
    P = Ps[k]
    n = ns[k]
    sum_scores = np.zeros(epoch_count)
    epoch = 0
    while epoch<epoch_count:
        p = random.random()
        if random.random()<p: #start with the information that first coin was Tails
            continue
        tosses = 2*(np.random.random((1,n+1))<p)-1 #make first toss be H to induce our assumption
        tosses[0,0] = -1 #make first toss be H to induce our assumption, we will need to remove this first H from our score later
        Hs = (tosses==1).astype(np.int32)
        sum_tosses = np.cumsum(tosses)
        sum_Hs = np.cumsum(Hs)
        stop_ind = np.where(sum_tosses<-1*P[sum_Hs])[0]
        stop_ind = -1 if stop_ind.shape[0]==0 else stop_ind[0]
        score = sum_tosses[stop_ind]+1 #add the score removed from assumption
        sum_scores[epoch] = sum_scores[epoch-1]+score
        if epoch%100000==99999:
            print(epoch+1, n, sum_scores[epoch]/(epoch+1), time.time()-start)
        epoch += 1
    sum_scores_ns.create_dataset(str(n),data=sum_scores)

sum_scores_ns.close()
