import matplotlib as mpl
from matplotlib.widgets import RectangleSelector
import numpy as np
import argparse 
from matplotlib import pyplot as plt
import pandas as pd

import sys
sys.path.append('../interaction')

from brush import Brush
import legend
from random import Random

from numpy.typing import ArrayLike

def linscale(values, vmin, vmax):
    _min = values.min()
    _max = values.max()
    v = vmin + (values-_min)/(_max-_min)*(vmax-vmin)
    return v

def get_cax(fig, colname):
    for a in fig.get_axes():
        if (a.get_xlabel() is not None and a.get_xlabel() == colname) or \
           (a.get_ylabel() is not None and a.get_ylabel() == colname):
           return a
    return fig.get_axes()[-1]

class BubbleChart:
    def __init__(self,
                 x=None, y=None, s=None, c=None,
                 xname='x', yname='y', sname='size', cname='color',
                 fig=None, ax=None, cax=None, sax=None,
                 figsize=(10,8), minsize=50, maxsize=500,
                 cmap='viridis'):
        """
        Create a bubble chart

        Parameters
        ----------
        x, y, s, c : `ArrayLike`
            The array-like objects containing the x, y, size, and color 
            parameters of the bubble chart.

        xname, yname, sname, cname : `str`
            The names of the variables corresponding to x, y, size, and color 
            to display in legends.

        fig : `~matplotlib.Figure`
            The figure in which the bubble chart and its legends is drawn.

        ax : `~matplotlib.axes.Axes`
            The `~.axes.Axes` instance in which the bubble chart is drawn.

        cax : `~matplotlib.axes.Axes`
            The `~.axes.Axes` instance in which the colorbar is drawn.

        sax : `~matplotlib.axes.Axes`
            The `~.axes.Axes` instance in which the size legend is drawn.

        figsize :` 2-tupple`
            The size of the figure (ignored if `fig` is provided)

        minsize, maxsize : `float`
            The range of bubble sizes that the `s` values will be mapped to.
        """
        # depending on the info provided, create a layout
        # 1. Do we have an active figure?
        if fig is not None:
            self.fig = fig 
            # 2. Do we have an active Axes?
            if ax is not None:
                self.ax = ax
                self.cax = cax
                self.sax = sax
            # 3. If not, does the active figure contain an Axes we could use?
            elif self.fig.get_axes():
                self.ax = self.fix.get_axes()[0]
                self.cax = cax
                self.sax = sax
            # Otherwise, we will create our own layout within the existing figure
            else:
                all_axes = \
                fig.subplot_mosaic([['plot', 'size'], ['plot', 'color']], 
                                   width_ratios=[0.85, 0.12], height_ratios=[0.4, 0.6], gridspec_kw={ 'wspace': 0.03 })
                self.ax = all_axes['plot']
                self.cax = all_axes['color']
                self.sax = all_axes['size']
        # If no figure is given, we will create our own layout from scratch
        else:
            self.fig, all_axes = \
                plt.subplot_mosaic([['plot', 'size'], ['plot', 'color']], 
                                   width_ratios=[0.85, 0.12], height_ratios=[0.4, 0.6], gridspec_kw={ 'wspace': 0.03 })
            self.ax = all_axes['plot']
            self.cax = all_axes['color']
            self.sax = all_axes['size']

        [ self.x, self.y, self.s, self.c ] = [ x, y, s, c ]
        self.sizes = None
        self.size_range = [ minsize, maxsize ]
        self.scale = 1
        [ self.xname, self.yname, self.sname, self.cname ] = \
            [ xname, yname, sname, cname ] 
        [ self.plot_bg, self.plot, self.colorbar, self.legend ] = [ None ]*4
        self.selected = []
        self.cmap = mpl.colormaps[cmap].resampled(256)
        if self.s is not None: self.update_sizes()
    
    def update_sizes(self):
        self.sizes = np.array(linscale(self.s, self.size_range[0], 
                                               self.size_range[1]))
        self.sizes *= self.scale

    def set_data(self, var: str, data: ArrayLike, name: str|None=None):
        if name is None: name = var
        match var.lower():
            case 'x':
                self.x = data
                self.xname = name 
                return
            case 'y':
                self.y = data 
                self.yname = name 
                return 
            case 'c' | 'color' | 'colors':
                self.c = data 
                self.cname = name 
                return 
            case 's' | 'size' | 'sizes':
                self.s = data
                self.sname = name 
                self.update_sizes()
                return
            
    def draw(self):
        for a in [ self.plot, self.plot_bg, self.legend ]:
            if a is not None:
                a.remove()
        # We will redraw whatever remains of the artists in this Axes,
        # e.g. a brushing rectangle
        to_redraw = self.ax._children
        self.ax.clear()
        # colorbar is a special case: removing it will destroy 
        # the Axes that contains it. We will clear that axes instead
        # to preserve the container.
        if self.cax is not None:
            self.cax.clear()
        
        if self.x is None or \
           self.y is None or \
           self.c is None or \
           self.sizes is None:
            raise ValueError('One of the attributes is not defined')

        if self.selected:
            # if a selection was made, we will render in two steps:
            # Step 1: non-selected points in uniform gray 
            # Step 2: selected points in their native colors
            mask = np.ones(self.x.shape[0], dtype=bool)
            mask[self.selected] = False
            x_masked = self.x[mask]
            y_masked = self.y[mask]
            s_masked = self.sizes[mask]
            x_shown = self.x[self.selected]
            y_shown = self.y[self.selected]
            s_shown = self.sizes[self.selected]
            c_shown = self.c[self.selected]
            self.plot_bg = self.ax.scatter(x_masked, y_masked, 
                                           color=(0.9,0.9,0.9), s=s_masked,
                                           edgecolors=(0.9,0.9,0.9))
            # Note: we specify the value range so that the colors of the
            # selected data points do not change
            self.plot = self.ax.scatter(x_shown, y_shown, c=c_shown, s=s_shown, 
                                        vmin=np.min(self.c),
                                        vmax=np.max(self.c),
                                        edgecolors='black', cmap=self.cmap)
        else:
            # otherwise, straight passing of attributes to scatterplot
            self.plot_bg = None
            self.plot = self.ax.scatter(self.x, self.y, c=self.c, s=self.sizes, 
                                        edgecolors='black', cmap=self.cmap)

        # Redraw the artists that are not owned by this bubble chart
        for a in to_redraw:
            self.ax.add_artist(a)

        self.ax.set_xlabel(self.xname, weight='bold')
        self.ax.set_ylabel(self.yname, weight='bold')
        if self.cax is not None:
            self.colorbar = self.fig.colorbar(self.plot, cax=self.cax,
                                              label=self.cname)
        else:
            # we were given a figure and an Axes but no cax:
            # matplotlib will now create one for us.
            self.colorbar = self.fig.colorbar(self.plot, ax=self.ax,
                                              label=self.cname)
            self.cax = get_cax(self.fig, self.cname)

        if self.sax is not None:
            # if a specific Axes was provided, we will draw the legend in it
            sax = self.sax
            sax.axis('off')
            loc='upper left'
            offset=(0,1)
        else:
            # otherwise we draw it over the plot
            sax = self.ax
            loc='upper right'
            offset = (1,1)
        self.legend = legend.make_size_legend(self.s, self.sizes, nstops=3, 
                                              title=self.sname, spacing=1.5, 
                                              log_scale=False, ax=sax, 
                                              facecolor=self.cmap(0.5),
                                              loc=loc, offset=offset)
        self.fig.draw(self.fig._get_renderer())

class interaction:
    def __init__(self, chart):
        self.chart = chart 
    
    def update(self, selected):
        chart.selected = selected 
        chart.draw()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Demonstrate bubble chart')
    parser.add_argument('-n', '--number', type=int, default=100, help='Number of data points')
    parser.add_argument('--brush', action='store_true', help='Activate brush selector')
    args = parser.parse_args()
    
    x = np.random.rand(args.number)
    y = np.random.rand(args.number)
    c = np.random.rand(args.number)
    s = np.random.rand(args.number)

    chart = BubbleChart(x=x, y=y, s=s, c=c, xname='x', yname='y', 
                        sname='size', cname='colors', fig=None)

    inter = interaction(chart)

    if args.brush:
        brush = Brush(x, y, chart.ax, inter.update, color='blue')
    chart.draw()
    plt.show()