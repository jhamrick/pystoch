import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.stats

def _plot(title=None, axis=None, path=None, legend=False):
    fontsize = 50
    
    if title is not None:
        plt.title(title, fontsize=fontsize)
    
    if legend:
        plt.legend(prop={'size': fontsize}, loc=0)

    ax = plt.gca()
    ax.grid(True)
    ax.set_axisbelow(True)

    for tick in ax.xaxis.get_major_ticks():
        tick.set_pad(10.)
        tick.label1 = tick._get_text1()
        tick.label1.set_fontsize(fontsize)
        
    for tick in ax.yaxis.get_major_ticks():
        tick.set_pad(20.)
        tick.label1 = tick._get_text1()
        tick.label1.set_fontsize(fontsize)

    fig = plt.gcf()
    fig.subplots_adjust(left=0.15)

    if path is None:
        plt.show()
    else:
        save(path)


def _discrete_hist(samples, binkeys=None):
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

def discrete_hist(samples, title, labels=None, ymax=None, path=None):
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
        binkeys, binvals = _discrete_hist(samps[bar])
        all_binkeys = all_binkeys.union(binkeys)
    all_binkeys = list(all_binkeys)
    all_binkeys.sort()

    max_height = 0

    for bar in xrange(num_bars):
        binkeys, binvals = _discrete_hist(samps[bar], all_binkeys)
        
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

def cont_hist(samples, title, numbins=20, labels=None, ymax=None, path=None):
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

def line_plot(x, y, title, labels=None, path=None):

    xmin = np.min(x)
    ymin = np.min(y)
    xmax = np.max(x)
    ymax = np.max(y)

    kwargs = {}
    if labels is not None:
        kwargs['label'] = labels
    plt.plot(x, y, **kwargs)

    _plot(title=title, legend=(labels is not None), path=path)
        
def print_discrete_hist(samples):
    binkeys, binvals = _discrete_hist(samples)

    for key, val in zip(binkeys, binvals):
        print "%s\t%s" % (key, val)

# save a figure from pyplot
def save(path, width=16.5, height=16.5):
    fig = plt.gcf()
    fig.set_figwidth(width)
    fig.set_figheight(height)

    directory = os.path.split(path)[0]
    filename = os.path.split(path)[1]
    if directory == '':
        directory = '.'

    if not os.path.exists(directory):
        os.makedirs(directory)

    print "Saving figure to '" + os.path.join(directory, filename) + "'...", 
    plt.savefig(os.path.join(directory, filename))
    plt.clf()
    plt.cla()
    plt.close()
    print "Done"
