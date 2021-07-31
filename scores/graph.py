import matplotlib.pyplot as plt
import numpy as np
import matplotlib

data = np.loadtxt('scores.txt', unpack='False')

unique, counts = np.unique(data, return_counts=True)
counts = counts/len(data) * 100
count = dict(zip(unique, counts))
print("number of samples where activity score is not \"N/A\": ", len(data))
print("percentage of total samples (in percent): " , count)

bins = [0, 0.5, 1.0, 1.5, 2, 2.5]

plt.hist(data, histtype='bar', bins = bins)
plt.xlabel('CYP2D6 activity score')
plt.ylabel('Amount of samples')
plt.title('Distribution of activity scores')
plt.legend()
plt.show()
