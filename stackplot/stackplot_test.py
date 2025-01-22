import matplotlib
from matplotlib import pyplot as plt

from datetime import datetime, timedelta

import numpy as np

from stackplot import stackplot

show = False # Open plot window.
save = True  # Save plot to file.

rcParams = {
              'savefig.dpi': 300,
              'savefig.format': 'png',
              #'savefig.bbox': 'standard',
              'savefig.transparent': False,

              'figure.max_open_warning': 50,
              'figure.figsize': (8.5, 11),
              'figure.dpi': 150,

              # Note: use constrained_layout here instead of fig.tight_layout().
              # It is more flexible and can be set with rc_context parameters.
              # https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html
              'figure.constrained_layout.use': True,
              # Padding (height/width) between edges of adjacent subplots,
              # Pad on top and bottom of figure
              #'figure.constrained_layout.h_pad': 0.04167,
              # Vertical gap between subplots
              #'figure.constrained_layout.hspace': 0.02,
              # Pad on left and right of figure
              #'figure.constrained_layout.w_pad': 0.04167,
              # Horizontal gap between subplots
              #'figure.constrained_layout.wspace': 0.02,

              # Ignored if constrained_layout is True.
              #'figure.subplot.bottom': 0.11,
              #'figure.subplot.hspace': 0.2,
              #'figure.subplot.left': 0.125,
              #'figure.subplot.right': 0.9,
              #'figure.subplot.top': 0.88,
              #'figure.subplot.wspace': 0.2,

              'axes.titlesize': 10,
              'axes.grid': True,
              'font.family': 'serif',
              'mathtext.fontset': 'dejavuserif'
          }

#print(matplotlib.rcParamsDefault)

def plot(tn, t, y, title, style, max_gap, rcParams):

  title = f"#{tn}: {title}"
  with matplotlib.rc_context(rc=rcParams):
    fig = stackplot(t, y, title=title, style=style, max_gap=max_gap)

    plt.draw()
    if show:
      plt.show()
    if save:
      plt.savefig(f"stackplot_test/stackplot_test_{tn:02d}.png")

    return fig

t1 = [datetime(2000,1,1,0,0,20) + timedelta(seconds=i) for i in range(20)]
y1 = np.arange(0, 20)
s1 = {'color': 'black', 'linestyle': '-'}

t2 = [datetime(2000,1,1,0,0,0) + timedelta(seconds=i) for i in range(20)]
y2 = y1
s2 = {'color': 'green', 'marker': '.', 'markerfacecolor': 'red', 'markeredgecolor': 'red', 'linestyle': '-'}

t2g = t2.copy()
y2g = list(y2).copy()
for gap in [18, 10, 1]:
  t2g.pop(gap)
  y2g.pop(gap)
y2g = np.array(y2g)

# t and y structure
title = "#1: t = [datetimes] and y = [ints]"
plot(1, list(t1), list(y1), title, s1, None, rcParams)

title = "t = [datetimes] and y = [[ints], [ints]]"
plot(2, list(t1), [list(y1), list(y1+1)], title, s1, None, rcParams)

title = "t = [[datetimes], [datetimes]] and y = [[ints], [ints]]"
plot(3, [list(t1), list(t1)], [list(y1), list(y1+1)], title, s1, None, rcParams)

title = "t = [[datetimes], [datetimes]] and y = [[ints], [ints, ints]]"
plot(4, [list(t1), list(t2)], [list(y1), [list(y2), list(y2+1)]], title, s1, None, rcParams)

# Gaps
title = "t = [datetimes w/gaps] and y = [ints]"
plot(5, list(t2g), list(y2g), title, s1, timedelta(seconds=1), rcParams)

# Title
title = "t = [datetimes], y = [[ints], [ints]], title = [str, str]"
plot(6, list(t1), [list(y1), list(y1+1)], title, s1, None, rcParams)

# Style
title = "t = [datetimes], y = [[ints], [ints]], style = [dict, dict]"
plot(7, list(t1), [list(y1), list(y1+1)], title, [s1, s2], None, rcParams)

# Spacing of subplots
_rcParams = rcParams.copy()
_rcParams['figure.constrained_layout.use'] = True

# https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.set_constrained_layout_pads.html
# Height padding in inches (above and below padding)
_rcParams['figure.constrained_layout.h_pad'] = 0.04
# Height spacing in between subplots in fraction of the subplot height
_rcParams['figure.constrained_layout.hspace'] = 0.05
# Width padding in inches (left and right padding)
_rcParams['figure.constrained_layout.w_pad'] = 0.04

title = "h_pad = 0.04 in, hspace = 0.05, w_pad = 0.04 in"
fig = plot(8, list(t1), [list(y1), list(y1+1)], title, [s1, s2], None, _rcParams)

_rcParams['figure.constrained_layout.hspace'] = 0.1
_rcParams['figure.constrained_layout.w_pad'] = 0.1
title = "h_pad = 0.04 in, hspace = 0.10, w_pad = 0.10 in"
fig = plot(9, list(t1), [list(y1), list(y1+1)], title, [s1, s2], None, _rcParams)

_rcParams['figure.constrained_layout.h_pad'] = 0.4
_rcParams['figure.constrained_layout.w_pad'] = 0.4
title = "h_pad = 0.40 in, hspace = 0.10, w_pad = 0.40 in"
fig = plot(10, list(t1), [list(y1), list(y1+1)], title, [s1, s2], None, _rcParams)
