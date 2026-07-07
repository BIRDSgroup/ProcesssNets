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
from Functions import centrality

# %% Input
arg = sys.argv
tissue = arg[1]
B = int(arg[2])
gfolder = arg[3]

metadata = pd.read_csv(tissue + '/edge count.tsv', header=None, index_col=0, sep='\t')
n = metadata.loc[0, 1]
del metadata

out_file = tissue + '/trivial pr.csv'
# %% Computing the Closeness Centrality
for b in range(B):
    edges = np.genfromtxt('graphs_' + gfolder + '/' + str(b) + '.csv', delimiter=',', dtype=int)
    
    G = nx.from_edgelist(edges)
    G.add_nodes_from(range(n))
    
    pr_dict = nx.algorithms.link_analysis.pagerank(G, tol=1e-05)
    pr = []
    for v in range(n):
        pr.append(pr_dict[v])
    
    with open(out_file, 'a') as op_file:
        print(b, *pr, sep=',', end='\n', file=op_file)
    op_file.close()
