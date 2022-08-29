import numpy as np
import matplotlib.pyplot as plt

data_0H0T = np.load('./10000000Trials/avg_scores_100_1000_10000.npy')
data_1H0T = np.load('./10000000Trials/avg_scores_100_1000_10000_with_1H0T.npy')
data_0H1T = np.load('./10000000Trials/avg_scores_100_1000_10000_with_0H1T.npy')

data = [data_0H0T, data_1H0T, data_0H1T]
titles = ['0H0T', '1H0T', '0H1T']
ns = [100,1000,10000]
avgPerNs = [
        [0.2265971031730966,0.24490450115379334,0.24905537083629034,0.25],
        [0.4018486612383934,0.41330665099425146,0.4160149920742702,0.4166666666666667],
        [0.0561675346135595,0.07699905917240113,0.08214570168004924,0.08333333333333333]
        ]

plt.rcParams["figure.figsize"] = (12,4)
fig, axes = plt.subplots(1,3)

fig.suptitle('Average Return on n Tosses')
fig.supxlabel('log10(Number of Trials)')
fig.supylabel('Average Return per n')

for k in range(3):
    d = data[k]
    ax = axes[k]
    n = ns[k]
    title = titles[k]
    avgPerN = avgPerNs[k]
    for j in range(3):
        ax.plot(np.log10(np.arange(10001,d.shape[1]+1)), d[j,10000:]/n, linewidth=0.5, label='n={n}'.format(n=n))
        ax.axhline(y=avgPerN[j], color='r', linestyle='--', linewidth=1)
    ax.axhline(y=avgPerN[-1], color='m', linestyle='--', linewidth=1)
    ax.set_title(title)
plt.savefig('Average Return on n Tosses.png', bbox_inches='tight')
