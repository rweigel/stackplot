import datetime

import numpy as np
from matplotlib.ticker import MaxNLocator, MultipleLocator

from datetick import datetick

def stackplot(t, y, title=None, style=None, max_gap=None):

  from matplotlib import pyplot as plt

  if isinstance(y[0], list):
    n_stack = len(y)
    print(f"y has {len(y)} list elements => n_stack = len(y) = {len(y)}")
    t = _check_and_expand_t(y, t)
    style = _check_and_expand_style(y, style)
  else:
    n_stack = 1
    print("y has values => n_stack = 1.")

  if isinstance(title, list) and len(title) > 1 and len(title) != n_stack:
    raise ValueError(f'len(title) = {len(title)} != len(y) = {n_stack}')

  plt.figure()
  gs = plt.gcf().add_gridspec(n_stack)
  axes = gs.subplots(sharex=True)
  if n_stack == 1:
    axes = [axes]

  if not isinstance(y[0], list):
    print(f"  y has {len(y)} values")
    _plot(t, y, axes[0], style, max_gap)
    axes[0].set_title(title)
    if _all_int(y):
      axes[0].yaxis.set_major_locator(MaxNLocator(integer=True))
      axes[0].yaxis.set_major_locator(MultipleLocator(1))
    return plt.gcf()

  for i in range(0, len(y)):

    if isinstance(title, list):
      axes[i].set_title(title[i])
    if isinstance(title, str) and i == 0:
      axes[i].set_title(title)

    if isinstance(y[i][0], list):
      print(f"  y[{i}] has {len(y[i])} list elements")
      t[i] = _check_and_expand_t(y[i], t[i])
      style[i] = _check_and_expand_style(y[i], style[i])
      for j in range(0, len(y[i])):
        if 'label' not in style:
          style[i][j]['label'] = f'$y_{{{j}}}$'
        _plot(t[i][j], y[i][j], axes[i], style[i][j], max_gap)
      axes[i].legend()
    else:
      print(f"  y[{i}] has {len(y[i])} values")
      _plot(t[i], y[i], axes[i], style[i], max_gap)
      if 'label' in style[i]:
        axes[i].set_ylabel(style[i]['label'])

    if i == n_stack - 1:
      datetick('x', axes=axes[i])

  return plt.gcf()

def _all_int(y):

  y = np.array(y)
  Ig = ~np.isnan(y)
  if np.all(np.equal(y[Ig], np.int32(y[Ig]))):
    return True
  else:
    return False

def _plot(t, y, axis, style, max_gap):

    if max_gap is not None:
        t, y = _insert_nans(t, y, max_gap)

    axis.plot(t, y, **style)

    line = axis.lines[0]
    line_marker = line.get_marker()
    if max_gap is not None and line_marker == 'None':
        line_width = line.get_linewidth()
        if len(y) > 3:
            line_style = {
                            "marker": '.',
                            "markersize": 1.5*line_width,
                            "color": line.get_color()
                        }
            # If second or second to last value is NaN, plot a marker at that point.
            if np.isnan(y[-2]):
                axis.plot(t[-1], y[-1], **line_style)
            if np.isnan(y[1]):
                axis.plot(t[0], y[0], **line_style)

def _check_type(y, _type):

    for i in range(0, len(y)):
        if not isinstance(y[i], _type):
            return i

    return True

def _check_and_expand_style(y, style):
    if isinstance(y[0], list):
        if isinstance(style, dict):
            _style = []
            for i in range(0, len(y)):
                _style.append(style)
            style = _style
        else:
            if len(style) != len(y):
                raise ValueError(f'len(style) = {len(style)} != len(y) = {len(y)}')
    else:
        if isinstance(style, list):
            raise ValueError('If y is not a list, style must not be a list. style is a list.')

    return style

def _check_and_expand_t(y, t):

    if isinstance(y[0], list):
        # y = [list, list, ...] # Each list is plotted on the same axis.
        _ret = _check_type(y, list)
        if _ret is not True:
            raise ValueError(f'If y[0] is a list, all elements of y must be lists. Element y[{_ret}] is not a list.')

        if isinstance(t[0], list):
            # t = [list, list, ...]
            _ret = _check_type(t, list)
            print(f"t has {len(t)} list elements")
            if _ret is not True:
                raise ValueError(f'If t[0] is a list, all elements of t must be lists. Element t[{_ret}] is not a list.')
            if len(t) != len(y):
                raise ValueError(f'len(t) = {len(t)} != len(y) = {len(y)}')
        else:
            print("t has values. Using same t for each in list element in y.")
            _t = []
            if len(t) != len(y[0]):
                raise ValueError(f'len(t) = {len(t)} != len(y[0]) = {len(y[0])}')
            for i in range(0, len(y)):
                _t.append(t)
            t = _t
    else:
        if isinstance(t[0], list):
            raise ValueError('If y is not a list, t must not be a list. t is a list.')

    return t

def _insert_nans(t, y, dt_min):
    """Insert NaNs in time series where time difference is greater than dt_min"""
    _t = []
    _y = []
    for i in range(0, len(t) - 1):
      dt = t[i+1] - t[i]
      _t.append(t[i])
      _y.append(y[i])
      if dt > dt_min:
        _t.append(t[i+1] - datetime.timedelta(microseconds=1))
        _y.append(np.nan)
    _t.append(t[-1])
    _y.append(y[-1])

    return _t, _y
