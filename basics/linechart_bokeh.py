from bokeh.plotting import figure, show
import numpy as np
import math

x = np.linspace(-5*math.pi, 5*math.pi, 200)
# print(x)
y = [ math.sin(u)/u for u in x ]

p = figure(title="Sinc curve", x_axis_label='x', y_axis_label='y')
# add a line renderer with legend and line thickness to the plot
p.line(x, y, legend_label="Sinc", line_width=2)
show(p)