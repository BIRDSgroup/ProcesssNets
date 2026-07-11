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
from networkx.algorithms import closeness_centrality

# %% Input
arg = sys.argv
tissue = arg[1]
B = int(arg[2])
gfolder = arg[3]

metadata = pd.read_csv(tissue + '/edge count.tsv', header=None, index_col=0, sep='\t')
n = metadata.loc[0, 1]
del metadata

out_file = tissue + '/trivial cc.csv'
# %% Computing the Closeness Centrality
for b in range(B):    
    edges = np.genfromtxt('graphs_' + gfolder + '/' + str(b) + '.csv', delimiter=',', dtype=int)
    
    G = nx.from_edgelist(edges)
    G.add_nodes_from(range(n))
    
    cc = closeness_centrality(G)
    cc_sorted = [0]*n
    for k in range(n):
        cc_sorted[k] = cc[k]
    
    with open(out_file, 'a') as op_file:
        print(b, *cc_sorted, sep=',', end='\n', file=op_file)
    op_file.close()
    