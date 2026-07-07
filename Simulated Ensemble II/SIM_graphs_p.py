# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 14:45:55 2024

@author: HP
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import networkx as nx
from time import time

# %% Global Variables / Inputs
import sys

arg = sys.argv
folder = arg[1]
n = int(arg[2])
B = 1000

# p-values = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5]

# %% Network Constructor Function
def ConstructNetwork(n,seeds=None):
    print('Generating the networks')
    for b in range(B):
        deg_seq = np.round(nx.utils.powerlaw_sequence(n=n, seed=seeds[b], exponent=2.5)).tolist()
        G = nx.expected_degree_graph(deg_seq, seed=seeds[b], selfloops=False)        
        #G = nx.gnp_random_graph(n=n, p = p/100, seed=seeds[b])
        edges = np.array(G.edges())
        
        op_folder = str(n)
        np.savetxt(op_folder + '/' + str(b) + '.csv', edges, delimiter=',', fmt='%d')
        with open(op_folder + '/edge count.tsv', 'a') as ec_file:
            print(b, n, len(edges), sep='\t', file=ec_file)
        ec_file.close()
    return

# %% Seed
import os
seed_file = 'Model/' + folder + '/seed.txt'
if not os.path.exists(seed_file):
    seed = int(time())
    with open(seed_file, 'w') as file:
        print(seed, file = file)
    file.close()
else:
    with open(seed_file, 'r') as file:
        seed = int(file.read())
    file.close()

rng = np.random.default_rng(seed=seed)
seeds = rng.integers(0, 2**32-1, size=B).tolist()
ConstructNetwork(n,seeds=seeds)
'''
# %% Main Part
for p in [1, 5, 10, 15, 20, 25, 50]:
    if not os.path.exists(str(p)):
        os.makedirs(str(p))
    ConstructNetwork(n,p,seeds=seeds)
'''
