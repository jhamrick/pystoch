"""
pystoch.graphing.histogram
--------------------------

"""

import numpy as np
import matplotlib.pyplot as plt
from .utils import _plot

def _hist(samples, binkeys=None):
    bins = {}
    for sample in samples:
        if sample not in bins:
            bins[sample] = 0
        bins[sample] += 1

    if binkeys is None:
        binkeys = bins.keys()
        binkeys.sort()

    binvals = []
    for key in binkeys:
        if key in bins:
            binvals.append(bins[key])
        else:
            binvals.append(0)

    return binkeys, binvals

def hist(samples, title, labels=None, ymax=None, path=None):
    samps = np.array(samples)
    if len(samps.shape) == 1:
        samps = samps[None, ...]
    if len(samps.shape) > 2:
        raise ValueError, "invalid size of input array"
    num_bars = samps.shape[0]

    overall_width = 0.8
    colors = ['b', 'g', 'r', 'c', 'm', 'y']

    all_binkeys = set()
    for bar in xrange(num_bars):
        binkeys, binvals = _hist(samps[bar])
        all_binkeys = all_binkeys.union(binkeys)
    all_binkeys = list(all_binkeys)
    all_binkeys.sort()

    max_height = 0

    for bar in xrange(num_bars):
        binkeys, binvals = _hist(samps[bar], all_binkeys)
        
        width = overall_width / num_bars
        left = np.arange(len(binkeys)) + (width * bar)
        height = binvals

        if np.max(height) > max_height:
            max_height = np.max(height)

        kwargs = {}
        kwargs['color'] = colors[bar%len(colors)]
        if labels is not None:
            kwargs['label'] = labels[bar]

        plt.bar(left, height, width, **kwargs)

    left = np.arange(len(all_binkeys))
    if ymax is None:
        ymax = max_height * 1.10

    plt.xticks(np.arange(len(all_binkeys)) + (overall_width / 2.0), all_binkeys)

    axis = [left[0] - (overall_width / 2.0), left[-1] + (3.0 * (overall_width / 2.0)), 0, ymax]
    _plot(title=title, axis=axis, legend=(labels is not None), path=path)

def truehist(samples, title, numbins=20, labels=None, ymax=None, path=None):
    samps = np.array(samples)
    if len(samps.shape) > 2:
        raise ValueError, "invalid size of input array"
    num_bars = samps.shape[0]

    minval = np.min(samps)
    maxval = np.max(samps)

    kwargs = {}
    kwargs['bins'] = numbins
    kwargs['range'] = (minval, maxval)
    if labels is not None:
        kwargs['label'] = labels
    plt.hist(samps.transpose(), **kwargs)

    _plot(title=title, legend=(labels is not None), path=path)
