import numpy as np
import pandas as pd
import math

import matplotlib.pyplot as plt

X = np.random.normal(0, 1, 1000)


plt.hist(X)
plt.title("Gaussian Histogram")
plt.xlabel("Returns")
plt.ylabel("Frequency")

# the histogram of the data
# n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)

fig = plt.gcf()

plt.plot(X, color='black')

Y_0 = math.log(40)
Y = [Y_0]
#dt = 1/252
z = 0.85
gamma = 1.15
sigma = [0.2]
for i in range(1, 10000):
    
    Y.append(Y[i-1] + sigma[i-1] * np.random.randn()) 
    
    sum = 0.0
    max_lags = min(i,30)
    for t in range(1, max_lags):
        sum = sum + ((Y[i] - Y[i - t])**2 / t ** gamma)
    
    sigma.append(sigma[0] * math.sqrt((1 + z * sum))) 

y_returns = []
for i in range(1, 10000):
    y_returns.append(Y[i]-Y[i-1])

X = np.random.normal(0, 1, 10000)
plt.hist(X, bins=50, facecolor='green', log=True)
plt.hist(y_returns, bins=50, facecolor='red', log=True)
#plt.plot(y_returns)