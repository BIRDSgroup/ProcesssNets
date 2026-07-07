# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 02:21:11 2026

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
    
# %% Muscle-Skeletal Tissue
folder = '../Muscle_Skeletal/'
nRange = range(100,1100,100)

JSI = pd.Series(index=nRange, dtype=float)
for n in nRange:
    filepath = folder + str(n)
    JSI[n] = readFile(filepath)
JSI.to_csv('mpjs.csv', header=['MPJS'], index=True)
