from hapiclient import hapi, hapitime2datetime
from stackplot import stackplot
import matplotlib

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

server     = 'https://cdaweb.gsfc.nasa.gov/hapi'
dataset    = 'OMNI_HRO_1MIN'
parameters = 'BX_GSE,BY_GSM,BZ_GSM,Vx,Vy,Vz,SYM_H'
start      = '2024-05-10T00:00:00Z'
stop       = '2024-05-15T00:00:00.000Z'

data, meta = hapi(server, dataset, parameters, start, stop)
time = hapitime2datetime(data['Time'])
tn = 1
with matplotlib.rc_context(rc=rcParams):
  fig = stackplot(time, [data['BZ_GSM'], data['SYM_H']])
fig.axes[0].grid(True)
fig.savefig(f"stackplot_test/stackplot_hapi_{tn:02d}.png")
print(f"Wrote stackplot_test/stackplot_hapi_{tn:02d}.png")
