import matplotlib.pyplot as plt
from cycler import cycler

ayu_mirage_plot_colors = [
    '#ffd173', '#5ccfe6', '#f28779', '#dfbfff', '#d5ff80',
    '#f07171', '#39bae6', '#ffb454', '#86b300', '#4cbf99',
    '#f07178', '#fa8d3e', '#ffad66', '#a37acc', '#f29668',
    '#7fd962', '#59c2ff', '#399ee6', '#73d0ff', '#ff7383'
]

theme = {
    'axes.facecolor': '#1f2430',
    'figure.facecolor': '#1f2430',
    'text.color': '#cbccc6',
    'axes.labelcolor': '#cbccc6',
    'xtick.color': '#cbccc6',
    'ytick.color': '#cbccc6',
    'axes.edgecolor': '#5c6773',
    'grid.color': '#5c6773',
    'axes.grid': True,
    'font.size': 12,
    'axes.prop_cycle': cycler(color=ayu_mirage_plot_colors)
}

