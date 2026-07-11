# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 05:57:39 2025

@author: HP
"""

from Functions.envVar import setThreads
setThreads()

# %% Packages
import pandas as pd
import numpy as np
import sys
from time import time

from Functions import centrality

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

out_file = tissue + '/mytrivial degree.csv'
# %% Computing the Degree
for b in range(B):
    st = time()
    edges = np.genfromtxt('graphs_' + gfolder + '/' + str(b) + '.csv', delimiter=',', dtype=int)
    i += (time() - st)
    degree = centrality.DegreeCentrality(edges, n)
    st = time()
    with open(out_file, 'a') as op_file:
        print(b, *degree, sep=',', end='\n', file=op_file)
    op_file.close()
    o += (time() - st)

p = (time()-start) - i - o
print('i = ', i, 'p = ', p, 'o = ', o, sep='\t')