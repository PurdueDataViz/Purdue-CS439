import numpy as np
from bokeh.plotting import figure, output_file, show

# Data for plotting
t = np.arange(-5.0*np.pi, 5.0*np.pi, 0.01)
s = np.sin(t)/t

output_file('sinc.html')

p = figure(title = 'Sinc function', x_axis_label = 'x', y_axis_label = 'sin(x)/x')

p.line(t, s, line_width=2)
show(p)
