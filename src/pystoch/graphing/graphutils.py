"""
pystoch.graphing.graphutils
---------------------------

"""

import numpy as np
import matplotlib.pyplot as plt
import os

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
