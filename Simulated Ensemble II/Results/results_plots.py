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
    3: 'pagerank'
}

#colors = ['#000000', '#0072B2', '#E69F00', '#009E73', '#CC79A7', '#A5796B']
colors = ['#949494', '#000000'] + list(sns.color_palette("colorblind", n_colors=5).as_hex())
symbols = ["circle", "circle-open", "cross", "square-open", "square", "diamond", "diamond-open"]
plt_shapes = ['o', 's', '*', 'X', 'P', '^', 'v']

madi_linenos = {
    0: 3,
    1: 8,
    2: 15,
    3: 20
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

def plot2D(DFs, measure_idx, x_ticks, y_ticks, x_axis, y_axis):
    plt.figure()
    for idx in range(len(Algos)):
        rows = []
        for it in DFs.keys():
            rows.append(DFs[it].iloc[idx,:])
        df = pd.concat(rows, axis=1)
        Y_mean = df.mean(axis=1)
        Y_std = df.std(axis=1)
        plt.errorbar(
            Y_mean.index, Y_mean, 
            yerr=Y_std, 
            label = Algos[idx], 
            color=colors[idx], 
            marker=plt_shapes[idx], fmt='o', 
            ecolor='grey', elinewidth=1.5,
            capsize=2, capthick=1)
    plt.legend(loc="upper right", bbox_to_anchor=(1.48, 1), title='Algorithms', fontsize=12) 
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(x_axis, fontsize=16)
    plt.ylabel('Running Time (in secs)', fontsize=16)
    plt.title(properties[measure_idx], fontsize=18)
    #plt.tight_layout()
    plt.savefig('2D_' + properties[measure_idx] + '.pdf', bbox_inches="tight")
    plt.close()

# %% 2D plots
nRange = range(100,1100,100)
for measure_idx in properties.keys():
    if measure_idx == 0:
        continue
    DFs = dict()
    for it in range(1,4):
        folder = '../p' + str(it) + '/'
        DF = pd.DataFrame(index=FileNames, columns=nRange, dtype=float)
        for i, method in enumerate(FileNames):
            lineno = madi_linenos[measure_idx] if i >= 2 else trivial_linenos[measure_idx]
            for n in nRange:
                filename = folder + str(n) + '/' + method + '.txt'
                DF.loc[method, n] = readFile(filename, lineno)
        DFs[it] = DF
    plot2D(DFs, measure_idx, DF.columns, Algos, 'n', 'Algorithms')
