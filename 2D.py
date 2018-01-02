import csv
import numpy as np
import pandas as pd
from time import time
from bokeh.models import BoxAnnotation
from bokeh.client import push_session
from bokeh.plotting import figure, curdoc
from bokeh.layouts import WidgetBox, column, row
from bokeh.models.widgets import Panel, Tabs, Select


#filename = input("Enter a file name: ")
filename = 'stocks.csv'
file = open(filename, 'r')
csvCursor = csv.reader(file)

is_header = True
input_data = dict()
header = []

start = time()

# declare figure #     
p1 = figure(toolbar_location=None,output_backend="webgl", plot_height=1000, plot_width=1000)
p1.xaxis.major_label_orientation = np.pi/4
# p2 = figure(toolbar_location=None)
# p2.xaxis.major_label_orientation = np.pi/4
# p3 = figure(toolbar_location=None,output_backend="webgl")
# p3.xaxis.major_label_orientation = np.pi/4

# open a session to keep our local document in sync with server
#session = push_session(curdoc())

for r in csvCursor:
    if is_header:
        # store keys in dict #
        header = r
        for i in range(len(r)):
            input_data[r[i]] = []

        # change labels of x-axes and y-axes
        p1.xaxis.axis_label = header[0]
        # p2.xaxis.axis_label = header[0]
        # p3.xaxis.axis_label = header[0]
        #p.yaxis.axis_label = header[1]

        is_header = False
    else:
        #if test>0:
        for i in range(len(r)):
            if i==0: # store year #
                tmp = r[i].split('-')
                year = ''
                for it in tmp:
                    year += it
                input_data[header[i]].append(int(year))
            else:
                input_data[header[i]].append(float(r[i]))
        #test -= 1

start_i = end_i = 0
# start_j = end_j = 0
# start_k = end_k = 0

cir = p1.circle(x=[], y=[])
# bar = p2.vbar(x=[],top=[], width=0.5)
# lin = p3.circle(x=[], y=[])

dc = cir.data_source
# db = bar.data_source
# dl = lin.data_source

# y1 = Select(title='Y-Axis', options=['None']+header[1:])
# y2 = Select(title='Y-Axis', options=['None']+header[1:])
# y3 = Select(title='Y-Axis', options=['None']+header[1:])

# controls1 = WidgetBox(y1, width=150)
# controls2 = WidgetBox(y2, width=150)
# controls3 = WidgetBox(y3, width=150)

# group1 = row(controls1, p1)
# group2 = row(controls2, p2)
# group3 = row(controls3, p3)

# panel #

# def p1_callback(attr, old, new):
#     if y1.value==header[1]:
#         curdoc().add_periodic_callback(cir_callback_1, 50)
#     elif y1.value==header[2]:
#         curdoc().add_periodic_callback(cir_callback_2, 50)
    #curdoc().add_periodic_callback(bar_callback, 50)
    #curdoc().add_periodic_callback(lin_callback, 50)

def cir_callback():
    global start_i, end_i
    if end_i<len(input_data['Date']):

        new_data = dict()
        new_data['x'] = dc.data['x'] + input_data['Date'][start_i:end_i]
        new_data['y'] = dc.data['y'] + input_data['Open'][start_i:end_i]

        if int((input_data['Date'][start_i])/10000) >= 1988:
            box = BoxAnnotation(left=input_data['Date'][start_i], right=input_data['Date'][end_i], fill_color='red', fill_alpha=0.1)
            p1.add_layout(box)
        # if int(input_data['Date'][start_i]/10000) <= 1962:
            
        #     end = time()
        #     print ('total time: ', end-start)
        dc.data = new_data

        start_i = end_i
        end_i += 50

# def bar_callback():
#     global start_j, end_j
#     new_data = dict()
#     new_data['x'] = db.data['x'] + input_data['Date'][start_j:end_j]
#     new_data['top'] = db.data['top'] + input_data['Open'][start_j:end_j]
    
#     db.data = new_data

#     start_j = end_j
#     end_j += 50

# def lin_callback():
#     global start_k, end_k
#     new_data = dict()
#     new_data['x'] = dl.data['x'] + input_data['Date'][start_k:end_k]
#     new_data['y'] = dl.data['y'] + input_data['Open'][start_k:end_k]

#     dl.data = new_data

#     start_k = end_k
#     end_k += 50

curdoc().add_periodic_callback(cir_callback, 50)
# curdoc().add_periodic_callback(bar_callback, 50)
# curdoc().add_periodic_callback(lin_callback, 50)

curdoc().add_root(p1)
#session.show(tabs)
#session.loop_until_closed() # run forever