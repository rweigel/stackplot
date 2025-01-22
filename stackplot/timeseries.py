import datetime
import warnings

import numpy as np
import matplotlib

from datetick import datetick

# https://github.com/pandas-dev/pandas/issues/18301
# Suppresses depreciation warning.
# TODO: determine what version of pandas this is needed for.
# Observed in Matplotlib 3.0, pandas 0.25.3, Python 3.5.
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def timeseries(t, y, **kwargs):
    """Plot a time series"""

    opts = {
                'logging': False,
                'title': '',
                'xlabel': '',
                'ylabel': '',
                'logx': '',
                'logy': '',
                'nodata': False,
                'backend': 'default',
                'returnimage': False,
                'transparent': False,
                'legendlabels': []
            }

    for key, value in kwargs.items():
        if key in opts:
            opts[key] = value
        else:
            warnings.warn('Warning: Ignoring invalid keyword option "%s".' % key, SyntaxWarning)

    if opts['returnimage']:
        # When returnimage=True, the Matplotlib OO API is used b/c it is thread safe.
        # Otherwise, the pyplot API is used. Ideally would always use the OO API,
        # but this has problems with notebooks and showing figures when executing
        # a script from the command line.
        # TODO: Document issues.
        #
        # API differences description:
        # https://www.saltycrane.com/blog/2007/01/how-to-use-pylab-api-vs-matplotlib-api_3134/
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        if opts['logging']:
            from matplotlib import __version__ as mpl_version
            print("timeseries(): Using Matplotlib %s with FigCanvasAgg back-end" % mpl_version)
    else:
        from matplotlib import pyplot as plt
        if opts['backend'] != 'default':
            try:
                matplotlib.use(opts['backend'], force=True)
            except:
                matplotlib.use(matplotlib.get_backend(), force=True)
                warnings.warn('Warning: matplotlib(' + opts['backend'] + \
                              ') call failed. Using default backend of ' + 
                              matplotlib.get_backend(), SyntaxWarning)

        if opts['logging']:
            from matplotlib import __version__ as mpl_version
            print("timeseries(): Using Matplotlib %s with %s back-end" % (mpl_version, matplotlib.get_backend()))

    if not isinstance(y, np.ndarray) and len(y) > 1 and len(y[0] > 1):
        y = np.array(y).T
    else:
        y = np.array(y)

    t = np.array(t)

    if y.shape[0] != t.shape[0]:
        if len(y.shape) > 1:
            if y.shape[1] == t.shape[0]:
                y = y.T
            if len(t.shape) > 1 and y.shape[0] == t.shape[1]:
                y = y.T

    if y.shape[0] < 11:
        props = {'linestyle': 'none', 'marker': '.', 'markersize': 16}
    elif y.shape[0] < 101:
        props = {'linestyle': '-', 'linewidth': 2, 'marker': '.', 'markersize': 8}
    else:
        props = {}

    ylabels = []

    if issubclass(y.dtype.type, np.flexible):
        # See https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.scalars.html
        # for diagram of subclasses.
        # Find unique strings and give each an integer value.
        # Modify tick labels to correspond to unique strings
        yu = np.unique(y)
        if len(yu) > 20:
            # Too many labels in this case. One option is to find
            # number of unique first characters and change labels to
            # "first character" and then warn. If number of unique first
            # characters < 21, try number of unique second characters, etc.
            raise ValueError('Can only plot strings if number of unique strings < 21')
        yi = np.zeros((y.shape))
        for i in range(0, len(yu)):
            yi[y == yu[i]] = i
        ylabels = yu
        y = yi


    # Can't use matplotlib.style.use(style) because not thread safe.
    # Set context using 'with'.
    # Setting stylesheet method: https://stackoverflow.com/a/22794651/1491619
    if opts['returnimage']:
        # See note above about OO API for explanation for why this is
        # done differently if returnimage=True
        fig = Figure()
        # Attach canvas to fig, which is needed by datetick and hapiplot.
        FigureCanvas(fig) 
        ax = fig.add_subplot(111)
    else:
        fig, ax = plt.subplots()

    if len(y.shape) > 1:
        all_nan = np.full((y.shape[1]), False)
        for i in range(0, y.shape[1]):
            try:
                all_nan[i] = np.all(np.isnan(y[:,i]))
            except:
                all_nan[i] = False
    else:
        all_nan = np.array([False])
        try:
            all_nan[0] = np.all(np.isnan(y))
        except:
            all_nan[0] = False

    legendlabels = opts['legendlabels'].copy()
    if legendlabels == []:
        if len(y.shape) > 1:
            for i in range(0, y.shape[1]):
                legendlabels.append('col #{}'.format(i))

    if np.any(all_nan):
        if legendlabels != []:
            if len(y.shape) > 1:
                for i in range(0, y.shape[1]):
                    if all_nan[i] == True and opts['nodata'] == False:
                        legendlabels[i] = '{0:s}: All {1:d} values are NaN'.format(legendlabels[i], y.shape[0])
                    else:
                        legendlabels[i] = '{0:s}: No data in interval'.format(legendlabels[i])
            else:
                if opts['nodata'] == True:
                    legendlabels[0] = '{0:%s}: No data in interval'.format(legendlabels[0])
                else:
                    legendlabels[0] = '{0:%s}: All {1:d} values are NaN'.format(legendlabels[0], y.shape[0])
        else:
            if len(y.shape) > 1:
                for i in range(0, y.shape[1]):
                    if all_nan[i] == True and opts['nodata'] == False:
                        legendlabels[i] = 'All {0:d} values are NaN'.format(y.shape[0])
                    else:
                        legendlabels[i] = 'No data in interval'
            else:
                if opts['nodata'] == True:
                    legendlabels =  ['No data in interval']
                else:
                    legendlabels =  ['All {0:d} values are NaN'.format(len(y))]

    if np.all(all_nan):
        ax.set_yticklabels([])
        ax.set_yticks([])

    if len(y) == 1:
        ax.set_yticks(y)

    if np.any(all_nan):
        if len(y.shape) > 1:
            for i in range(0, y.shape[1]):
                if all_nan[i]:
                    ax.plot([t[0],t[-1]],[0,0], alpha=0)
                else:
                    ax.plot(t, y[:,i])
        else:
            ax.plot([t[0],t[-1]],[0,0], linestyle=None, alpha=0)
    else:
        ax.plot(t, y, **props)

    ax.set(ylabel=opts['ylabel'], xlabel=opts['xlabel'], title=opts['title'])
    try:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-3,3), useMathText=True)
    except:
        pass

    if legendlabels != []:
        leg = fig.legend(legendlabels)

    if np.any(all_nan):
        for i in range(0, len(all_nan)):
            leg.get_lines()[i].set_alpha(1)

    ax.set_position([0.12,0.125,0.850,0.75])

    if np.all(all_nan):
        ax.grid(which='major', axis='x')
    else:
        ax.grid()

    if not np.all(all_nan) and len(ylabels) > 0:
        ax.set_yticks(np.unique(y))
        ax.set_yticklabels(ylabels)


    if isinstance(t[0], datetime.datetime):
        datetick('x', axes=ax)
    if isinstance(y[0], datetime.datetime):
        datetick('y', axes=ax)

    # savefig.transparent=True requires the following for the saved image
    # to have a transparent background. Seems as though figure.facealpha
    # and axes.facealpha should be rc parameters, but they are not. So
    # savefig.transparent controls both transparency in saved image and
    # in GUI image.
    if opts['transparent']:
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

    if not opts['returnimage']:
        plt.show()

    return fig

def adjust_labels(ax):
    # Not used. See
    # https://stackoverflow.com/questions/24581194/matplotlib-text-bounding-box-dimensions
    # for determining text bounding box in figure coordinates
    for item in ax.get_yticklabels():
        ml = 0 # max length
        for t in item.get_text().split('\n'):
            l = len(t)
            if l > ml: ml = l 
