import datetime

import numpy as np

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator

from datetick import datetick

def stackplot(t, y, title=None, style=None, max_gap=None):

  if not isinstance(y[0], list):
    y = [y]

  n_stack = len(y)
  t = _check_and_expand_t(y, t)
  style = _check_and_expand_style(y, style, dict)

  if isinstance(title, list) and len(title) > 1 and len(title) != n_stack:
    raise ValueError(f'len(title) = {len(title)} != len(y) = {n_stack}')

  plt.figure()
  gs = plt.gcf().add_gridspec(n_stack)
  axes = gs.subplots(sharex=True)
  if n_stack == 1:
    axes = [axes]

  for i in range(0, len(y)):

    if isinstance(title, list):
      axes[i].set_title(title[i])
    if isinstance(title, str) and i == 0:
      axes[i].set_title(title)

    if isinstance(y[i][0], list):
      print(f"  y[{i}] has {len(y[i])} list elements")
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

  if len(t) == 1:
    if 'marker' not in style:
      style['marker'] = '.'

  if len(t) < 10:
    if 'marker' not in style:
      style['marker'] = '.'

  axis.plot(t, y, **style)

  if _all_int(y):
    axis.yaxis.set_major_locator(MaxNLocator(integer=True))
    axis.yaxis.set_major_locator(MultipleLocator(1))

  line = axis.lines[0]
  line_marker = line.get_marker()
  line_width = line.get_linewidth()
  print(f"  line_marker = {line_marker}")
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
      raise ValueError(f'y[{i}] is not a {_type}')

  return True

def _check_and_expand_style(y, style, inner):

  if inner is dict:
    if style is None:
      # style = None
      style = [{}]
    if isinstance(style, dict):
      # style = {}
      style = [style]

  if len(style) == 1 and len(y) > 1:
    # y = [list, list, ...]
    # style = [[dict]] => style = [dict, dict, ...]
    style = style*len(y)

  # y = [list, list, ...]
  # style = [dict, dict, ...]
  # or
  # style = [list of dicts, list of dicts, ...]

  if len(style) != len(y):
    if len(style) == 1:
      # y = [list, list, ...]
      # style = [dict]
      style = style*len(y)
      # style = [dict, dict, ...]
    else:
      raise ValueError(f'len(style) = {len(style)} != len(y) = {len(y)}')

  for i in range(0, len(y)):
    if isinstance(style[i], inner) and isinstance(y[i][0], list):
      # y = [[list, list], ...]
      # style = [dict, ...]
      style[i] = [style[i]]*len(y[i])
    if len(style[i]) == 1 and len(y[i]) > 1:
      # y = [[list, list], ...]
      # style = [[dict], ...]
      style[i] = _check_and_expand_style(y[i], style[i][0])
    if isinstance(style[i], list):
      # style = [list of dicts, list of dicts, ...]
      if len(style) != len(y):
        raise ValueError(f'len(style[{i}]) = {len(style[i])} != len(y[{i}]) = {len(y[i])}')

  return style

def _check_and_expand_style_test():

  y1 = [[1]]
  y2 = [[1], [1]]
  y3 = [[[1], [1]], [1]]

  so = None
  s = _check_and_expand_style(y1, so, dict)
  print(f"y = {y1}; style = {so} => {s}")
  assert(s == [{}])

  s = _check_and_expand_style(y2, so, dict)
  print(f"y = {y2}; style = {so} => {s}")
  assert(s == [{}, {}])
  s = _check_and_expand_style(y3, so, dict)
  print(f"y = {y3}; style = {so} => {s}")
  assert(s == [[{}, {}], {}])


  so = {}
  s = _check_and_expand_style(y1, so, dict)
  print(f"y = {y1}; style = {so} => {s}")
  assert(s == [{}])

  s = _check_and_expand_style(y2, so, dict)
  print(f"y = {y2}; style = {so} => {s}")
  assert(s == [{}, {}])

  s = _check_and_expand_style(y3, so, dict)
  print(f"y = {y3}; style = {so} => {s}")
  assert(s == [[{}, {}], {}])


  so = [{}]
  s = _check_and_expand_style(y1, so, dict)
  print(f"y = {y1}; style = {so} => {s}")
  assert(s == [{}])

  s = _check_and_expand_style(y2, so, dict)
  print(f"y = {y2}; style = {so} => {s}")
  assert(s == [{}, {}])

  s = _check_and_expand_style(y3, so, dict)
  print(f"y = {y3}; style = {so} => {s}")
  assert(s == [[{}, {}], {}])

  so = [{}, {}]
  s = _check_and_expand_style(y2, so, dict)
  print(f"y = {y2}; style = {so} => {s}")
  assert(s == [{}, {}])

  so = [[{}, {}], {}]
  s = _check_and_expand_style(y3, so, dict)
  print(f"y = {y3}; style = {so} => {s}")
  assert(s == [[{}, {}], {}])

def _check_and_expand_t(y, t):

  # y = [list, list, ...] # Each list is plotted on the same axis.
  _ret = _check_type(y, list)
  if _ret is not True:
    raise ValueError(f'If y[0] is a list, all elements of y must be lists. Element y[{_ret}] is not a list.')

  if isinstance(t[0], list):
    # t = [list, list, ...]
    _ret = _check_type(t, list)
    print(f"  t has {len(t)} list elements")
    if _ret is not True:
      raise ValueError(f'If t[0] is a list, all elements of t must be lists. Element t[{_ret}] is not a list.')
    if len(t) != len(y):
      raise ValueError(f'len(t) = {len(t)} != len(y) = {len(y)}')
  else:
    print("  t has values. Using same t for each in list element in y.")
    if len(t) != len(y[0]):
      raise ValueError(f'len(t) = {len(t)} != len(y[0]) = {len(y[0])}')
    t = [t]*len(y)

  for i in range(0, len(y)):
    if isinstance(y[i][0], list):
      t[i] = _check_and_expand_t(y[i], t[i])

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

if __name__ == '__main__':
  _check_and_expand_style_test()
