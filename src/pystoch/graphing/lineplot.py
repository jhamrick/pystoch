"""
pystoch.graphing.lineplot
-------------------------

"""

import numpy as np
import matplotlib.pyplot as plt
from .graphutils import _plot

def lineplot(x, y, title, labels=None, path=None):

    xmin = np.min(x)
    ymin = np.min(y)
    xmax = np.max(x)
    ymax = np.max(y)

    kwargs = {}
    if labels is not None:
        kwargs['label'] = labels
    plt.plot(x, y, **kwargs)

    _plot(title=title, legend=(labels is not None), path=path)
