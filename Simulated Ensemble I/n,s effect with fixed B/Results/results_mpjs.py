# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 10:38:19 2026

@author: HP
"""

# %% Global Variables
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['text.usetex'] = True

#import plotly.graph_objects as go
#import plotly.io as pio
#pio.renderers.default = "browser"

Algos = [
    r"\texttt{trivial}-self",
    r"\texttt{trivial}-networkx",
    r"\texttt{\textsc{ProcessNets}}-rstar",
    r"\texttt{\textsc{ProcessNets}}-slink",
    r"\texttt{\textsc{ProcessNets}}-fpa",
    r"\texttt{\textsc{ProcessNets}}-upgma",
    r"\texttt{\textsc{ProcessNets}}-wpgmc"
    ]
FileNames = ['mytrivial', 'trivial', 'rstar', 'slink', 'fpa', 'upgma', 'wpgmc']

properties = {
    0: 'tree',
    1: 'degree',
    2: 'component size',
    3: 'pagerank',
    4: 'closeness'
}

#colors = ['#000000', '#0072B2', '#E69F00', '#009E73', '#CC79A7', '#A5796B']
colors = ['#949494', '#000000'] + list(sns.color_palette("colorblind", n_colors=5).as_hex())

# %% Functions
def readFile(filepath):
    with open(filepath + '/jsi.txt', 'r') as file:
        line = file.readline().strip()
        return round(float(line.split(' ')[-1]),2)

def heatmap(JSI, x_axis, y_axis, fname):
    plt.figure()
    sns.heatmap(JSI, annot=True, cmap='coolwarm')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title('Change in MPJS \n' + y_axis + ' vs. ' + x_axis)
    plt.savefig('mpjs_' + fname + '.pdf')
    plt.close()

# %% n v/s s
nRange = range(100,1100,100)
SampleSizes = [75, 100, 150, 200, 300, 500, 600, 700, 1000, 1500]

JSI_vals = dict()
for i in range(1,4):
    folder = '../s' + str(i) + '/'
    JSI = pd.DataFrame(index=nRange, columns=SampleSizes, dtype=float)
    for n in nRange:
        for s in SampleSizes:
            filepath = folder + str(n) + '/' + str(s)
            JSI.loc[n,s] = readFile(filepath)
    heatmap(JSI, 's', 'n', 's' + str(i))
    JSI_vals[i] = JSI
avg_jsi = (JSI_vals[1] + JSI_vals[2] + JSI_vals[3]) / 3
heatmap(avg_jsi, 's', 'n', 'avg')