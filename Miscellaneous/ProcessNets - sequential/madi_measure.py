# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 03:59:50 2025

@author: HP
"""

# %% Packages
import pandas as pd
import sys

from Functions import compute

# %% Input
arg = sys.argv
tissue = arg[1]
B = int(arg[2])
tree_type = arg[3]
measure = arg[4]
# measure = 'degree' | 'connectivity' | 'pr' | 'cc'

metadata = pd.read_csv(tissue + '/edge count.tsv', header=None, index_col=0, sep='\t')
n = metadata.loc[0, 1]
del metadata

folder = tissue + '/' + tree_type.upper() + '/'
out_file = tissue + '/' + tree_type + ' ' + measure + '.csv'

if measure == 'degree':
    compute.TreeDegree(folder, B, n, out_file, nonbinary=(tree_type=='rstar'))
elif measure == 'connectivity':
    compute.TreeConnectivity(folder, B, n, out_file, nonbinary=(tree_type=='rstar'))
elif measure == 'pr':
    compute.TreePageRank(folder, B, n, out_file, nonbinary=(tree_type=='rstar'))
elif measure == 'cc':
    compute.TreeCloseness(folder, B, n, out_file, nonbinary=(tree_type=='rstar'))
else:
    print('Invalid Measure')
