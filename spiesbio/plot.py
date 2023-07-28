import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import scipy
import seaborn as sns


class Grid:
    def __init__(self, n, ncols=5, width=4, height=4, constrained_layout=True):
        self.ncols = ncols
        self.nrows = int(np.ceil(n / ncols))

        self.width = width
        self.height = height

        total_width = self.ncols * self.width
        total_height = self.nrows * self.width

        self.fig, axes = plt.subplots(
            self.nrows,
            self.ncols,
            figsize=(total_width, total_height),
            constrained_layout=constrained_layout,
        )

        self.axes = np.reshape(axes, -1)

        for ax in self.axes:
            ax.axis("off")

        self.i = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.i is None:
            self.i = 0
        else:
            self.i += 1

        if self.i >= self.ncols * self.nrows:
            raise StopIteration

        self.axes[self.i].axis("on")
        sns.despine(ax=self.axes[self.i])

        return self.axes[self.i]

def scatter(x, y, xlabel=None, ylabel=None, correlation=None, pointsize=10, color="black", log=None, ax=None):
    if ax is None:
        ax = plt.gca()

    if correlation is not None:
        if correlation == "spearman":
            rho = scipy.stats.spearmanr(x,y).statistic
            r_string = f"$r_s={rho:.2f}"
        elif correlation == "pearson":
            rho = scipy.stats.pearsonr(x,y).statistic
            r_string = f"$r_p={rho:.2f}"
        else:
            raise 

    if xlabel is None:
        try:
            xlabel = x.name
        except AttributeError:
            pass
    if ylabel is None:
        try:
            ylabel = y.name
        except AttributeError:
            pass
            
    
    ax.scatter(x, y, s=pointsize, facecolors='none', edgecolors=color, linewidth=0.5)

    if correlation is not None:
        ax.text(0.02, 0.95, r_string, horizontalalignment='left', transform=ax.transAxes)

    if log is not None:
        if "x" in log:
            ax.set_xscale("log")
        if "y" in log:
            ax.set_yscale("log")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

def format_ticklabels(axes="xy", format="{x:,.0f}", ax=None):
    import matplotlib as mpl
    if ax is None:
        ax = plt.gca()
    if "x" in axes:
        ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter(format))

    if "y" in axes:
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter(format))

def better_ticker(x,pos):
    """Format axis tick label using scientific notation"""
    import matplotlib.ticker as ticker

    if x == 0: return "$0$"

    is_negative = x<0
    x = abs(x)
    exponent = int(np.log10(x))
    coeff = x/10**exponent

    if is_negative:
        coeff = -coeff
    
    return r"${:2.0f} \times 10^{{ {:2d} }}$".format(coeff,exponent)