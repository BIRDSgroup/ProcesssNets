# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 02:21:25 2026

@author: HP
"""

# %% Global Variables
import pandas as pd
import numpy as np
import os

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
    
def plot2D(DF, measure_idx, x_ticks, y_ticks, x_axis, y_axis):
    plt.figure()
    for i in range(len(DF.index)):    
        plt.scatter(DF.columns, DF.iloc[i,:], label = Algos[i], color=colors[i], marker=plt_shapes[i])
    plt.legend(loc="upper right", bbox_to_anchor=(1.48, 1), title=y_axis, fontsize=12)
    plt.xticks(rotation=90, fontsize=15)
    plt.xlabel(x_axis, fontsize=16)
    plt.ylabel('Running Time (in secs)', fontsize=16)
    plt.title(properties[measure_idx], fontsize=18)
    #plt.tight_layout()
    plt.savefig('2D_'  + properties[measure_idx] + '.pdf', bbox_inches="tight")
    plt.close()
    
# %% All Tissues
Tissues = ["Muscle_Skeletal", "Whole_Blood", "Skin_Sun_Exposed_Lower_leg", "Thyroid", "Lung", "Stomach", "Pancreas", "Pituitary", "Brain_Cerebellum", "Brain_Cortex"]
colNames = ["Muscle Skeletal", "Whole Blood", "Skin", "Thyroid", "Lung", "Stomach", "Pancreas", "Pituitary", "Brain Cerebellum", "Brain Cortex"]
for measure_idx in properties.keys():
    DF = pd.DataFrame(index=FileNames, columns=Tissues, dtype=float)
    for i, method in enumerate(FileNames):
        if measure_idx == 0 and i < 2:
            continue
        lineno = madi_linenos[measure_idx] if i >= 2 else trivial_linenos[measure_idx]
        for tissue in Tissues:
            filename = '../' + tissue + '/' + method + '.txt'
            DF.loc[method, tissue] = readFile(filename, lineno)
    #DF.fillna(value=0, inplace=True)
    DF.columns = colNames
    #plot2D(DF, measure_idx, DF.columns, Algos, 'Tissue', 'Algorithms')
    
    DF.index = Algos
    
    op_file = 'Runtimes.xlsx'
    with pd.ExcelWriter(
            op_file, 
            engine="openpyxl", 
            mode="a" if os.path.exists(op_file) else "w"
            ) as writer:
        DF.to_excel(writer, sheet_name=properties[measure_idx], header=True, index=True)