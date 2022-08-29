import numpy as np
import random
import matplotlib.pyplot as plt
import time

P_100 = np.load('P_100.npy')
P_1000 = np.load('P_1000.npy')
P_10000 = np.load('P_10000.npy')
Ps = [P_100, P_1000, P_10000]
ns = [100,1000,10000]
epoch_count=100000000
sum_scores_ns = np.zeros((3,epoch_count))

for k in range(3):
    start = time.time()
    P = Ps[k]
    n = ns[k]
    sum_scores = np.zeros(epoch_count)
    avg_scores = np.zeros(epoch_count)
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
        avg_scores[epoch] = sum_scores[epoch]/(epoch+1)
        if epoch%100000==99999:
            print(epoch, n, avg_scores[epoch], time.time()-start)
        epoch += 1
    sum_scores_ns[k,:]=sum_scores
    plt.plot(np.log10(np.arange(10001,epoch_count+1)), avg_scores[10000:]/n, linewidth=0.5, label='n={n}'.format(n=n))

np.save('sum_scores_100_1000_10000_with_0H1T.npy',sum_scores_ns)

plt.title('Average Return Under Optimal Play with 0H1T')
plt.xlabel('Log10(Trials)')
plt.ylabel('Average Return per n')
plt.legend()
plt.axhline(y=0.0561675346135595, color='r', linestyle='--', linewidth=1)
plt.axhline(y=0.07699905917240113, color='r', linestyle='--', linewidth=1)
plt.axhline(y=0.08214570168004924, color='r', linestyle='--', linewidth=1)
plt.axhline(y=0.08333333333333333, color='m', linestyle='--', linewidth=1)
plt.savefig('Average Return for each n with 0H1T.png', bbox_inches='tight')


