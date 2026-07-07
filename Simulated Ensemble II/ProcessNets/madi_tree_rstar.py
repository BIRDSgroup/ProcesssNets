# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 19:11:26 2025

@author: HP
"""

from Functions.envVar import setThreads
setThreads()

# %% Packages
import pandas as pd
import numpy as np
from collections import defaultdict
import os
import sys

# %% Inputs
arg = sys.argv
tissue = arg[1]
B = int(arg[2])
gfolder = arg[3]

metadata = pd.read_csv(tissue + '/edge count.tsv', header=None, index_col=0, sep='\t')
n = metadata.loc[0, 1]

outfolder = tissue + "/RSTAR"


# %% Tree Construction
metadata['level'] = metadata[2].copy()
parent = B
edge_counter = 0
levels = np.unique(metadata['level'])
while len(levels):
    l = levels[-1]
    nodes = list(metadata.loc[metadata['level'] == l,:].index)
    
    if len(nodes) == 1:
        if len(levels) == 1:
            break        
        metadata.loc[nodes[0], 'level'] = levels[-2]
        levels = np.unique(metadata['level'])
        continue
    
    terminals = defaultdict(set)
    for idx, child in enumerate(nodes):
        if os.path.getsize('graphs_' + gfolder + '/' + str(child) + '.csv'):
            cedges = pd.read_csv('graphs_' + gfolder + '/' + str(child) + '.csv', header=None, index_col=None, sep=',', dtype=int)
            terminals[child] = set(cedges[0]*n + cedges[1])
        else:
            terminals[child] = set()
        
    
    sets = list(terminals.values())
    sets.sort(key=len)
    lca = sets[0].copy()
    lca.intersection_update(*sets[1:])
    del sets
    #lca = set.intersection(*terminals.values())
    
    lca_edges = np.zeros(shape=(len(lca), 2), dtype=int)
    lca_edges[:,0] = np.array(list(lca)) // n
    lca_edges[:,1] = np.array(list(lca)) % n
    
    np.savetxt('graphs_' + gfolder + '/' + str(parent) + '.csv', lca_edges, delimiter=',', fmt='%d')
    with open(outfolder + '/child_count.tsv', 'a') as cc_file:
        print(parent, len(nodes), sep='\t', end='\n', file=cc_file)
    cc_file.close()
    
    for child in nodes:
        edge_counter += 1
        tedge_terminal = terminals[child].difference(lca)
        with open(outfolder + '/' + str(edge_counter) + '.csv', 'w') as tedge_file:
            print(*tedge_terminal, sep='\n', end='', file=tedge_file)
        tedge_file.close()
        
        with open(outfolder + '/info.tsv', 'a') as info_file:
            print(edge_counter, parent, child, len(tedge_terminal), sep='\t', end='\n', file=info_file)
        info_file.close()
       
    # Variables Update
    metadata.loc[parent, :] = [n, len(lca), len(lca)]
    metadata.drop(index = nodes, inplace=True)
    levels = np.unique(metadata['level'])
    parent += 1

np.savetxt(outfolder + '/root.csv', lca_edges, delimiter=',', fmt='%d')
