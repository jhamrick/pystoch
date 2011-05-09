import numpy as np
import matplotlib.pyplot as plt

def hist(samples, title):
    bins = {}
    for sample in samples:
        if str(sample) not in bins:
            bins[str(sample)] = 0
        bins[str(sample)] += 1

    binkeys = bins.keys()
    binkeys.sort()

    hist = []
    for key in binkeys:
        hist.append(bins[key])

    width = 0.8
    left = np.arange(len(binkeys))
    height = hist

    plt.bar(left, height, width)
    plt.title(title)
    plt.xticks(left + (width / 2.0), binkeys)
    plt.axis([left[0] - (width / 2.0), left[-1] + (3.0 * (width / 2.0)), 0, np.sum(height)])
    plt.show()

    
