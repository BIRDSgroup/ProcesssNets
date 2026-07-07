# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:39:16 2026

@author: HP
"""

# %% Global Variables
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['text.usetex'] = True

import plotly.graph_objects as go
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
    0: 'tree construction',
    1: 'degree',
    2: 'component size',
    3: 'pagerank',
    4: 'closeness'
}

#colors = ['#000000', '#0072B2', '#E69F00', '#009E73', '#CC79A7', '#A5796B']
colors = ['#949494', '#000000'] + list(sns.color_palette("colorblind", n_colors=5).as_hex())
symbols = ["circle", "circle-open", "cross", "square-open", "square", "diamond", "diamond-open"]
plt_shapes = ['o', 's', '*', 'X', 'P', '^', 'v']

madi_linenos = {
    0: 3,
    1: 8,
    2: 13,
    3: 18
}

trivial_linenos = {
    0: None,
    1: 3,
    2: 8,
    3: 13
}

# %% Functions if any
def readFile(filename, lineno):
    with open(filename, 'r') as file:
        line = file.readlines()[lineno-1]
        time = line.strip().split('\t')[-1].split('m')
        minutes = int(time[0])
        seconds = float(time[1].split('s')[0])
        return minutes * 60 + seconds
  
def plot2D(DF, measure_idx, x_ticks, y_ticks, x_axis, y_axis, n):
    plt.figure()
    for i in range(len(DF.index)):    
        plt.scatter(DF.columns, DF.iloc[i,:], label = Algos[i+1], color=colors[i+1], marker=plt_shapes[i+1])
    plt.legend(loc="upper right", bbox_to_anchor=(1.48, 1), title=y_axis, fontsize=12)    
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(x_axis, fontsize=16)
    plt.ylabel('Running Time (in secs)', fontsize=16)
    plt.title(properties[measure_idx], fontsize=18)
    #plt.tight_layout()
    plt.savefig('2D_' + str(n) + '_' + properties[measure_idx] + '.pdf', bbox_inches="tight")
    plt.close()

# %% n = 100, different s
folder = '../100/'
nRange = range(100,1100,100)
SampleSizes = [75, 100, 150, 200, 300, 500, 600, 700, 1000, 1500]

DF = pd.DataFrame(index=FileNames[1:], columns=SampleSizes, dtype=float)
for i, method in enumerate(FileNames):
    if i == 0:
        continue
    lineno = 8 if i >= 2 else 3
    for s in SampleSizes:
        filename = folder + str(s) + '/' + method + '.txt'
        DF.loc[method, s] = readFile(filename, lineno)
plot2D(DF, 4, DF.columns, Algos, 's', 'Algorithms', 100)

