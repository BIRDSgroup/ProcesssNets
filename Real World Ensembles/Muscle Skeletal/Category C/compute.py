#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 21:13:36 2024

@author: sugyani
"""

from Model.Functions.envVar import setThreads
setThreads(1)

# %% Packages
import pandas as pd
import numpy as np
import random
import sys

import bootstrap

# %% Input
arg = sys.argv
tissue = arg[1]
b = int(arg[2])
s_percent = int(arg[3])

folder = tissue
if '_' in tissue and tissue.split(sep='_')[-1].isdigit():
    folder = "_".join(tissue.split(sep='_')[:-1])
in_file = 'Original Dataset/Preprocessed Files/' + folder + '/' + tissue + '.csv'

# %% Set the Seeds
with open('seeds/seed_' + str(b) + '', 'r') as seed:
    random.seed(seed.read())
seed.close()

# %% Bootstrapping
gexp = pd.read_csv(in_file, sep = ',', header=0, index_col=0)

n, s = gexp.shape
edges = bootstrap.BootstrapSubSample(gexp.T, spercent=(s_percent/100))

np.savetxt('Model/graphs_' + str(s_percent) + '/' + str(b) + '.csv', edges, delimiter=',', fmt='%d')
with open('Model/' + str(s_percent)  + '/edge count.tsv', 'a') as ec_file:
    print(b, n, len(edges), sep='\t', file=ec_file)
ec_file.close()
