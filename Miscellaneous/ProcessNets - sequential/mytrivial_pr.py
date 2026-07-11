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

from scipy.sparse import csr_array
from Functions import centrality

# %% Input
arg = sys.argv
tissue = arg[1]
B = int(arg[2])
gfolder = arg[3]

metadata = pd.read_csv(tissue + '/edge count.tsv', header=None, index_col=0, sep='\t')
n = metadata.loc[0, 1]
del metadata

out_file = tissue + '/mytrivial pr.csv'
# %% Computing the Closeness Centrality
for b in range(B):
    edges = np.genfromtxt('graphs_' + gfolder + '/' + str(b) + '.csv', delimiter=',', dtype=int)
    
    A = np.zeros(shape=(n,n), dtype=int)
    A[edges[:,0],edges[:,1]] = A[edges[:,1],edges[:,0]] = 1
    D = np.sum(A, axis=0)
    
    _, y = centrality.PageRankCentrality(csr_array(A), D)
    D_tilde = centrality.ComputeDTilde(D)
    pr = D_tilde * y
    with open(out_file, 'a') as op_file:
        print(b, *pr, sep=',', end='\n', file=op_file)
    op_file.close()
