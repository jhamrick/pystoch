import numpy as np
import matplotlib.pyplot as plt

def _hist(samples):
    bins = {}
    for sample in samples:
        if str(sample) not in bins:
            bins[str(sample)] = 0
        bins[str(sample)] += 1

    binkeys = bins.keys()
    binkeys.sort()

    binvals = []
    for key in binkeys:
        binvals.append(bins[key])

    return binkeys, binvals

def hist(samples, title):
    plt.figure()
    binkeys, binvals = _hist(samples)
    
    width = 0.8
    left = np.arange(len(binkeys))
    height = binvals

    plt.bar(left, height, width)
    plt.title(title)
    plt.xticks(left + (width / 2.0), binkeys)
    plt.axis([left[0] - (width / 2.0), left[-1] + (3.0 * (width / 2.0)), 0, np.sum(height)])
    plt.show()

def print_hist(samples):
    binkeys, binvals = _hist(samples)

    for key, val in zip(binkeys, binvals):
        print "%s\t%s" % (key, val)
