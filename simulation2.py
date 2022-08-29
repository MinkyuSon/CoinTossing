import numpy as np
import random
import matplotlib.pyplot as plt
import time

P_100 = np.load('P_100.npy')
P_1000 = np.load('P_1000.npy')
P_10000 = np.load('P_10000.npy')
Ps = [P_100, P_1000, P_10000]
ns = [100,1000,10000]
epoch_count=1000000
avg_scores_ns = np.zeros((3,epoch_count))

for k in range(3):
    start=time.time()
    P = Ps[k]
    n = ns[k]
    sum_scores = [0]
    avg_scores = [0]
    for epoch in range(epoch_count):
        p = random.random()
        H = 0
        score = 0
        for toss in range(n):
            if np.random.random()<p:
                H += 1
                score += 1
            else:
                score -= 1
            if score < -1*P[H]:
                break
        sum_scores.append(score+sum_scores[-1])
        avg_scores.append(sum_scores[-1]/(epoch+1))
        if epoch%10000==0:
            print(epoch, n, avg_scores[-1], time.time()-start)
    avg_scores.pop(0)
    sum_scores.pop(0)
    avg_scores = np.array(avg_scores)/n
    avg_scores_ns[k,:]=avg_scores
    plt.plot(np.log10(np.arange(1001,epoch_count+1)), avg_scores[1000:], linewidth=0.5, label='n={n}'.format(n=n))

np.save('avg_scores_100_1000_10000.npy',avg_scores_ns)

plt.title('Average Return Under Optimal Play')
plt.xlabel('Log10(Trials)')
plt.ylabel('Average Return per n')
plt.legend()
plt.axhline(y=0.2266, color='r', linestyle='--', linewidth=1)
plt.axhline(y=0.2449, color='r', linestyle='--', linewidth=1)
plt.axhline(y=0.2491, color='r', linestyle='--', linewidth=1)



