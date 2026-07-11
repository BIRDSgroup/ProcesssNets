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

from Functions import connectivity

# %% DFS functions
def DFS(A, v):
    visited = [False] * n
    res = []
    
    stack = [v]
    while stack:
        node = stack.pop()
        if visited[node]:
            continue
        visited[node] = True
        res.append(node)        
        stack.extend(A[node][::-1])
    return res         

# %% Input
arg = sys.argv
tissue = arg[1]
B = int(arg[2])
gfolder = arg[3]

i = p = o = 0
start = time()

st = time()
metadata = pd.read_csv(tissue + '/edge count.tsv', header=None, index_col=0, sep='\t')
i += (time() - st)
n = metadata.loc[0, 1]
del metadata

out_file = tissue + '/mytrivial connectivity.csv'

# %% Computing the Connectivity
for b in range(B):
    st = time()
    edges = np.genfromtxt('graphs_' + gfolder + '/' + str(b) + '.csv', delimiter=',', dtype=int)    
    i += (time() - st)
    adj_list = {v: [] for v in range(n)}
    for e in edges:
        adj_list[e[0]].append(e[1])
        adj_list[e[1]].append(e[0])   
    
    visited = pd.Series([False]*n)
    compSizes = pd.Series([0]*n, dtype=int)
    for v in range(n):
        if not visited[v]:
            component = DFS(adj_list, v)
            visited[component] = True
            compSizes[component] = len(component)
    
    st = time()
    with open(out_file, 'a') as op_file:
        print(b, *compSizes, sep=',', end='\n', file=op_file)
    op_file.close()
    o += (time() - st)

p = (time()-start) - i - o
print('i = ', i, 'p = ', p, 'o = ', o, sep='\t')
