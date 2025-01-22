from hapiplot.plot.timeseries import timeseries
from datetime import datetime, timedelta
import numpy as np

T = 20
start = datetime(2000,1,1,0,0,0)
t = np.array([start + timedelta(seconds=i) for i in range(T)])
y = np.arange(0, T)

tests = [1,2,3,4,5]

for tn in tests:

    if tn == 1:
        title = 'test #' + str(tn) + ' All NaN values'
        timeseries(t, np.nan*y, title=title)

        title = 'test #' + str(tn) + ' All NaN values'
        timeseries(t, [np.nan*y,np.nan*y], title=title)

        title = 'test #' + str(tn) + ' All NaN values'
        timeseries(t, np.array([np.nan*y,np.nan*y]), title=title)

    if tn == 2:
        rcParams = {
                        'savefig.dpi': 144,
                        'savefig.format': 'png',
                        'savefig.bbox': 'standard',
                        'savefig.transparent': True,
                        'figure.max_open_warning': 50,
                        'figure.figsize': (8, 4.5),
                        'figure.dpi': 144,
                        'axes.titlesize': 12,
                        'font.family': 'serif',
                        'mathtext.fontset': 'dejavuserif'
                    }

        title = 'test #' + str(tn) + ' Using rc_context'
        from matplotlib import rc_context
        with rc_context(rc=rcParams):
            fig = timeseries(t, y, title=title)

    if tn == 3:
        title = 'test #' + str(tn) + ' Modify after render'
        fig = timeseries(t, y)
        fig.set_facecolor('gray')
        fig.axes[0].set_facecolor('yellow')
        fig.axes[0].set_ylabel('y label')

        # If any parts of the image are changed from the command line (i.e.,
        # after it has been rendered), you must enter "fig" on the command line
        # to re-render the image.

    if tn == 4:
        title = 'test #' + str(tn) + 'Stack plot'
        from matplotlib import rc_context
        T = 20
        t = np.array([start + timedelta(seconds=i) for i in range(T)])
        y = np.arange(0, T)
        y = np.vstack((y, y+1)).T
        rcParams['figure.figsize'] = (8.5, 11)
        with rc_context(rc=rcParams):
            fig = timeseries(t, y)

    if tn == 5:
        from matplotlib import rc_context
        # Ubuntu - type1cm package needed. Otherwise text.usetex fails
        rcParams = {'text.usetex': True}
        with rc_context(rc=rcParams):
            try:
                title = 'test #' + str(tn) + ' text.usetex=True w/o RuntimeError'
                fig = timeseries(t, y, title=title)
            except:
                failed = True
                pass

        # https://stackoverflow.com/questions/40894859/how-do-i-check-from-within-python-whether-latex-and-tex-live-are-installed-on-a
        rcParams = {'text.usetex': False}
        if failed:
            with rc_context(rc=rcParams):
                title = 'test #' + str(tn) + ' text.usetex=True gave RuntimeError'
                fig = timeseries(t, y, title=title)
