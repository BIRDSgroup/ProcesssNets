# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 05:57:39 2025

@author: HP
"""

from Functions.envVar import setThreads
setThreads()

# %% Packages
import numpy as np
import pandas as pd
import sys

import networkx as nx

# %% Input
arg = sys.argv
tissue = arg[1]
B = int(arg[2])
gfolder = arg[3]

metadata = pd.read_csv(tissue + '/edge count.tsv', header=None, index_col=0, sep='\t')
n = metadata.loc[0, 1]
del metadata

out_file = tissue + '/trivial degree.csv'
# %% Computing the Degree
for b in range(B):
    edges = np.genfromtxt('graphs_' + gfolder + '/' + str(b) + '.csv', delimiter=',', dtype=int)
    
    G = nx.from_edgelist(edges)
    G.add_nodes_from(range(n))
    
    degree = []
    for v in range(n):
        degree.append(G.degree[v])
    
    with open(out_file, 'a') as op_file:
        print(b, *degree, sep=',', end='\n', file=op_file)
    op_file.close()
