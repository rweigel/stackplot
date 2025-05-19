import datetime

import numpy as np

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator

from datetick import datetick

def stackplot(*args, title=None, style=None, max_gap=None):

  if len(args) < 2:
    t = None
    y = args[0]
  else:
    t = args[0]
    y = args[1]

  t = _check_and_expand_t(t, y)
  if not isinstance(y[0], list):
    y = [y]
  n_stack = len(y)
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

  yticks = axis.get_yticks()
  ylim_max = yticks[-1] # Force tick label above last y value.
  ylim_min = yticks[0]
  if ylim_min < 0 and min(y) >= 0:
    ylim_min = 0 # Prevent gap below 0 if no y values are negative.
  axis.set_ylim(ylim_min, ylim_max)

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
  else:
    pass

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
      style[i] = _check_and_expand_style(y[i], style[i][0], inner)
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

def _check_and_expand_t(t, y):

  if isinstance(t, np.ndarray):
    t = t.tolist()
  if isinstance(y, np.ndarray):
    y = y.tolist()
  if isinstance(y[0], np.ndarray):
    for i in range(0, len(y)):
      if isinstance(y[i], np.ndarray):
        y[i] = y[i].tolist()

  # y = [list, list, ...]
  if isinstance(y[0], list):
    _ret = _check_type(y, list)
    if _ret is not True:
      raise ValueError(f'If y[0] is a list, all elements of y must be lists. Element y[{_ret}] is not a list.')

  if t is None:
    t = []
    for i in range(0, len(y)):
      t.append([])
      if isinstance(y[i][0], list):
        for j in range(0, len(y[i])):
          #import pdb; pdb.set_trace()
          t[i].append(list(range(1, 1 + len(y[i][j]))))
      else:
        t[i] = list(range(1, 1 + len(y[i])))
    return t

  if not isinstance(t[0], list):
    if not isinstance(y[0], list):
      if len(t) != len(y):
        raise ValueError(f'len(t) = {len(t)} != len(y) = {len(y)}')
    if isinstance(y[0], list) and len(t) != len(y[0]):
        raise ValueError(f'len(t) = {len(t)} != len(y[0]) = {len(y[0])}')

  if isinstance(t[0], list) and not isinstance(y[0], list):
    raise ValueError('If t[0] is a list, y[0] must be a list.')

  if not isinstance(y[0], list):
    y = [y]
  if not isinstance(t[0], list):
    t = [t]
  if isinstance(t[0][0], list) and len(t[0]) == 1:
    t[0] = t[0][0]

  if not isinstance(t[0][0], list) and not isinstance(y[0][0], list):
    if len(t[0]) != len(y[0]):
      raise ValueError(f'len(t[0]) = {len(t[0])} != len(y[0]) = {len(y[0])}')

  if len(t) == 1 and len(y) > 1:
    # y = [list, list, ...]
    # t = [list] => t = [[list], [list], ...]
    t = t*len(y)
    for i in range(0, len(y)):
      if len(t[i]) != len(y[i]):
        raise ValueError(f'Cannot use same t for all y: len(t[0]) = {len(t[0])} != len(y[{i}]) = {len(y[i])}')
      if isinstance(y[i][0], list):
        t[i] = _check_and_expand_t([t[i]], y[i])
    return t

  if len(t) != len(y):
    raise ValueError(f'len(t) = {len(t)} != len(y) = {len(y)}')

  for i in range(0, len(y)):

    #print(i)
    #print(t[i])
    #print(y[i])

    if isinstance(t[i], list) and isinstance(t[i][0], list) and len(t[i]) > 1:
      if isinstance(y[i], list):
        if len(t[i]) != len(y[i]):
          raise ValueError(f'len(t[{i}]) = {len(t[i])} != len(y[{i}]) = {len(y[i])}')

      if not isinstance(y[i][0], list):
        raise ValueError(f't[{i}] is a list but y[{i}][0] is not')

    if isinstance(t[i][0], list) and len(t[0]) == 1:
      t[i] = t[i][0]

    if isinstance(y[i][0], list):
      t[i] = _check_and_expand_t([t[i]], y[i])
    else:
      if len(t[i]) != len(y[i]):
        raise ValueError(f'Cannot use same t for all y: len(t[{i}]) = {len(t[i])} != len(y[{i}]) = {len(y[i])}')

  return t

def _check_and_expand_t_test():

  y0 = [1, 2]
  y1 = [[1, 2]]
  y2 = [[1, 2], [3, 4]]
  y3 = [[[1, 2], [3, 4]], [5, 6]]
  y4 = [[[1, 2], [3, 4, 5]], [5, 6]]

  try:
    to = [1, 2, 3]
    t = _check_and_expand_t(to, y0)
    assert(False)
  except ValueError as e:
    print(f"y = {y0}; t = {to} => {e}")
    assert(e.args[0] == "len(t) = 3 != len(y) = 2")

  try:
    to = [1, 2, 3]
    t = _check_and_expand_t(to, y1)
    assert(False)
  except ValueError as e:
    print(f"y = {y1}; t = {to} => {e}")
    assert(e.args[0] == "len(t) = 3 != len(y[0]) = 2")

  to = None
  t = _check_and_expand_t(np.array(to), np.array(y1))
  print(f"y = {y1}; t = {to} => {t}")
  assert(t == [[1, 2]])

  to = None
  t = _check_and_expand_t(to, y1)
  print(f"y = {y1}; t = {to} => {t}")
  assert(t == [[1, 2]])

  t = _check_and_expand_t(to, y2)
  print(f"y = {y2}; t = {to} => {t}")
  assert(t == [[1, 2], [1, 2]])

  t = _check_and_expand_t(to, y3)
  print(f"y = {y3}; t = {to} => {t}")
  assert(t == [[[1, 2], [1, 2]], [1, 2]])

  t = _check_and_expand_t(to, y4)
  print(f"y = {y4}; t = {to} => {t}")
  assert(t == [[[1, 2], [1, 2, 3]], [1, 2]])


  to = [1, 2]
  t = _check_and_expand_t(to, y0)
  print(f"y = {y0}; t = {to} => {t}")
  assert(t == [[1, 2]])

  t = _check_and_expand_t(to, y1)
  print(f"y = {y1}; t = {to} => {t}")
  assert(t == [[1, 2]])

  t = _check_and_expand_t(to, y2)
  print(f"y = {y2}; t = {to} => {t}")
  assert(t == [[1, 2], [1, 2]])

  t = _check_and_expand_t(to, y3)
  print(f"y = {y3}; t = {to} => {t}")
  assert(t == [[[1, 2], [1, 2]], [1, 2]])


  to = [[1, 2]]
  try:
    t = _check_and_expand_t(to, y0)
    assert(False)
  except ValueError as e:
    print(f"y = {y0}; t = {to} => {e}")
    assert(e.args[0] == "If t[0] is a list, y[0] must be a list.")

  t = _check_and_expand_t(to, y1)
  print(f"y = {y1}; t = {to} => {t}")
  assert(t == [[1, 2]])

  t = _check_and_expand_t(to, y2)
  print(f"y = {y2}; t = {to} => {t}")
  assert(t == [[1, 2], [1, 2]])

  t = _check_and_expand_t(to, y3)
  print(f"y = {y3}; t = {to} => {t}")
  assert(t == [[[1, 2], [1, 2]], [1, 2]])


  to = [[[1, 2]]] # Interpreted same as to = [[1, 2]]
  t = _check_and_expand_t(to, y1)
  print(f"y = {y1}; t = {to} => {t}")
  assert(t == [[1, 2]])

  t = _check_and_expand_t(to, y2)
  print(f"y = {y2}; t = {to} => {t}")
  assert(t == [[1, 2], [1, 2]])

  t = _check_and_expand_t(to, y3)
  print(f"y = {y3}; t = {to} => {t}")
  assert(t == [[[1, 2], [1, 2]], [1, 2]])


  to = [[1, 2], [3, 4]]
  try:
    t = _check_and_expand_t(to, y1)
    assert(False)
  except ValueError as e:
    print(f"y = {y1}; t = {to} => {e}")
    assert(e.args[0] == "len(t) = 2 != len(y) = 1")

  t = _check_and_expand_t(to, y2)
  print(f"y = {y2}; t = {to} => {t}")
  assert(t == to)

  t = _check_and_expand_t(to, y3)
  print(f"y = {y3}; t = {to} => {t}")
  assert(t == [[[1, 2], [1, 2]] , [3, 4]])


  to = [[[1, 2]], [3, 4]] # Interpreted same as to = [[1, 2], [3, 4]]
  t = _check_and_expand_t(to, y3)
  print(f"y = {y3}; t = {to} => {t}")
  assert(t == [[[1, 2], [1, 2]], [3, 4]])

  to = [[[1, 2], [3, 4]], [5, 6]]
  t = _check_and_expand_t(to, y3)
  print(f"y = {y3}; t = {to} => {t}")
  assert(t == to)

  to = [[3, 4], [[1, 2]]] # Interpreted same as to = [[3, 4], [1, 2]]
  y3 = [[5, 6], [[1, 2], [3, 4]]]
  t = _check_and_expand_t(to, y3)
  print(f"y = {y3}; t = {to} => {t}")
  assert(t == [[3, 4], [[1, 2], [1, 2]]])

  to = [[5, 6], [[1, 2], [3, 4]]]
  y3 = [[[1, 2], [3, 4]], [5, 6]]
  try:
    t = _check_and_expand_t(to, y3)
    assert(False)
  except ValueError as e:
    print(f"y = {y3}; t = {to} => {e}")
    assert(e.args[0] == "t[1] is a list but y[1][0] is not")

  to = [[[1, 2], [3, 4]], [5, 6]]
  y3 = [[5, 6], [[1, 2], [3, 4]]]
  try:
    t = _check_and_expand_t(to, y3)
    assert(False)
  except ValueError as e:
    print(f"y = {y3}; t = {to} => {e}")
    assert(e.args[0] == "t[0] is a list but y[0][0] is not")

  y2 = [[1, 2], [3, 4, 5]]
  to = [[1, 2]]
  try:
    t = _check_and_expand_t(to, y2)
    assert(False)
  except ValueError as e:
    print(f"y = {y2}; t = {to} => {e}")
    assert(e.args[0] == "Cannot use same t for all y: len(t[0]) = 2 != len(y[1]) = 3")

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
  #_check_and_expand_style_test()
  _check_and_expand_t_test()
