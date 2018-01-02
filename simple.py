"""
read .csv files to visualize your data
"""

import csv
import numpy as np
import pandas as pd
from bokeh.client import push_session
from bokeh.plotting import figure, curdoc
from bokeh.layouts import WidgetBox, column, row
from bokeh.models.widgets import Panel, Tabs, Select
from bokeh.models import HoverTool

# filename = input("Enter a file name: ")
filename = 'stocks.csv'
file = open(filename, 'r')
csvCursor = csv.reader(file)

is_header = True
input_data = dict()
header = []

####### data input ########
for r in csvCursor:
    if is_header:
        # store keys in dict #
        header = r
        for i in range(len(r)):
            input_data[r[i]] = []

        is_header = False
    else:
        for i in range(len(r)):
            if i==0: # store year #
                tmp = r[i].split('-')
                year = ''
                for it in tmp:
                    year += it
                input_data[header[i]].append(int(year))
            else:
                input_data[header[i]].append(float(r[i]))

def create_figure_cir():
    xs = input_data[header[0]]
    ys = input_data[y1.value]
    x_title = header[0]
    y_title = y1.value

    kw = dict()

    hover = HoverTool(tooltips=[
        ('index', '$index'),
        ('(x, y)', '($x, $y)'),
    ])

    p = figure(**kw, tools=[hover], plot_height=1000, plot_width=1000)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    p.xaxis.major_label_orientation = pd.np.pi / 4
    p.circle(x=xs, y=ys, color='skyblue')

    return p

def create_figure_bar():
    xs = input_data[header[0]]
    ys = input_data[y2.value]
    x_title = header[0]
    y_title = y2.value

    kw = dict()

    hover = HoverTool(tooltips=[
        ('index', '$index'),
        ('(x, top)', '($x, $top)'),
    ])

    p = figure(**kw, tools=[hover], plot_height=1000, plot_width=1000)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    p.xaxis.major_label_orientation = pd.np.pi / 4
    p.vbar(x=xs, top=ys, width=0.5, color='pink')

    return p

def create_figure_lin():
    xs = input_data[header[0]]
    ys = input_data[y3.value]
    x_title = header[0]
    y_title = y3.value

    kw = dict()

    hover = HoverTool(tooltips=[
        ('index', '$index'),
        ('(x, y)', '($x, $y)'),
    ])

    p = figure(**kw, tools=[hover], plot_height=1000, plot_width=1000)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    p.xaxis.major_label_orientation = pd.np.pi / 4
    p.line(x=xs, y=ys, color='green')

    return p

def cir_update(attr, old, new):
    layout_cir.children[1] = create_figure_cir()

def bar_update(attr, old, new):
    layout_bar.children[1] = create_figure_bar()

def lin_update(attr, old, new):
    layout_lin.children[1] = create_figure_lin()

y1 = Select(title='Y-Axis', value=header[1], options=header[1:])
y2 = Select(title='Y-Axis', value=header[1], options=header[1:])
y3 = Select(title='Y-Axis', value=header[1], options=header[1:])

y1.on_change('value', cir_update)
y2.on_change('value', bar_update)
y3.on_change('value', lin_update)

controls1 = WidgetBox(y1, width=150)
controls2 = WidgetBox(y2, width=150)
controls3 = WidgetBox(y3, width=150)

layout_cir = row(controls1, create_figure_cir())
layout_bar = row(controls2, create_figure_bar())
layout_lin = row(controls3, create_figure_lin())

# panel #
tab1 = Panel(child=layout_cir, title="circle")
tab2 = Panel(child=layout_bar, title='vbar')
tab3 = Panel(child=layout_lin, title='line')

tabs = Tabs(tabs=[ tab1, tab2, tab3 ])

curdoc().add_root(tabs)