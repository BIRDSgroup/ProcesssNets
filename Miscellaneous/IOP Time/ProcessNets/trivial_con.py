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
from time import time

import networkx as nx

# %% Input
arg = sys.argv
tissue = arg[1]
B = int(arg[2])
gfolder = arg[3]

i = p1 = p2 = o = 0
start = time()

st = time()
metadata = pd.read_csv(tissue + '/edge count.tsv', header=None, index_col=0, sep='\t')
i += (time() - st)
n = metadata.loc[0, 1]
del metadata

out_file = tissue + '/trivial connectivity.csv'
# %% Computing the Connectivity
for b in range(B):
    st = time()
    edges = np.genfromtxt('graphs_' + gfolder + '/' + str(b) + '.csv', delimiter=',', dtype=int)
    i += (time() - st)
    
    visited = pd.Series([False]*n)
    compSizes = pd.Series([0]*n, dtype=int)
    
    st = time()
    G = nx.from_edgelist(edges)
    G.add_nodes_from(range(n))
    p1 += (time() - st)
    
    for v in range(n):
        if not visited[v]:
            component = list(nx.algorithms.dfs_preorder_nodes(G, v))
            visited[component] = True
            compSizes[component] = len(component)
    
    st = time()
    with open(out_file, 'a') as op_file:
        print(b, *compSizes, sep=',', end='\n', file=op_file)
    op_file.close()
    o += (time() - st)

p2 = (time()-start) - i - o - p1
print('i = ', i, 'p1 = ', p1, 'p2 = ', p2, 'o = ', o, sep='\t')