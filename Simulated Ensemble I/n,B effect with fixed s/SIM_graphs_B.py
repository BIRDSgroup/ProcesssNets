# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 14:45:55 2024

@author: HP
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests as fdr
import random
from time import time

# %% Global Variables / Inputs
import sys

arg = sys.argv
folder = arg[1]
n = int(arg[2])
s = int(arg[3])

# %% Co-expression Network Construction
def compute_edges(data):
    p = spearmanr(data)[1]
    indices = np.triu_indices(n, k=1)
    p_flat = p[indices]
    rejected, _, _, _ = fdr(p_flat, alpha=0.01, method='fdr_bh')
    
    adj_matrix = np.zeros((n,n))
    adj_matrix[indices] = rejected
    return np.argwhere(adj_matrix)

def Bootstrapping(data_sample):
    # data_sample.shape() = s x n
    print("Bootstrapping")
    for b in range(B):
        if b % 100 == 0:
            print(b)
        bootstrap_sample = data_sample.loc[random.choices(data_sample.index, k = s),:]
        edges = compute_edges(bootstrap_sample)
        
        op_folder = str(B)
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
random.seed(seed)
np.random.seed(seed)

# %% Population Dataset Generation
print('Population Dataset Generation')
pop_size = 1000000
data_pop = pd.DataFrame(index=range(pop_size))
for i in range(n//2):
    data_pop.loc[:,i] = np.random.normal(size = pop_size)

for i in range(n//2, n):
    deg = random.randint(1, n//2)
    chosen_vars = random.sample(range(n//2), k=deg)
    alpha = np.zeros(shape=(n//2 + 1,))
    alpha[chosen_vars] = 0.995
    alpha[-1] = 0.1
    beta = 0.01
    
    data_pop.loc[:,i] = pd.Series([1]*pop_size)
    noise = np.random.normal(size = pop_size)
    
    #data_pop[i] = data_pop.loc[:,range(n//2)] @ alpha[:-1] + (data_pop.loc[:,i] * alpha[-1]) + (beta * noise)
    
    data_pop.loc[:,i] = (data_pop.loc[:,i] * alpha[-1]) + (beta * noise)
    for j in range(n//2):
        data_pop.loc[:,i] += (data_pop.loc[:,j] * alpha[j])

# %% Observed and Bootstrap Dataset -- I
print('Observed Data Sampling')
data_sample = data_pop.loc[random.sample(list(data_pop.index), k=s), :]
del data_pop
for B in range(100, 1100, 100):
    if not os.path.exists(str(B)):
        os.makedirs(str(B))
    Bootstrapping(data_sample)