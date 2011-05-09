import numpy as np
import matplotlib.pyplot as plt

def hist(samples, title):
    bins = list(set(samples))
    bins.sort()
    bins.append(bins[-1]+1)

    hist, edges = np.histogram(samples, bins=bins)

    width = 0.8
    left = np.arange(len(bins[:-1]))
    height = hist

    plt.bar(left, height, width)
    plt.title(title)
    plt.xticks(left + (width / 2.0), bins[:-1])
    plt.axis([left[0] - (width / 2.0), left[-1] + (3.0 * (width / 2.0)), 0, np.sum(height)])
    plt.show()

    
