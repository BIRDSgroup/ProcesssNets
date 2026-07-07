# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 03:24:40 2025

@author: HP
"""

from Functions.envVar import setThreads
setThreads()

# %% Packages
import pandas as pd
import sys

from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform

from Functions import tree

# %% Inputs
arg = sys.argv
tissue = arg[1]
B = int(arg[2])
tree_type = arg[3]
gfolder = arg[4]

method = {
    'slink': 'single',
    'upgmc': 'centroid',
    'wpgmc': 'median',
    'fpa': 'complete',
    'upgma': 'average',
    'wpgma': 'weighted',
    'ward': 'ward'
}

metadata = pd.read_csv(tissue + '/edge count.tsv', header=None, index_col=0, sep='\t')
n = metadata.loc[0, 1]

# %% Main Function
D = tree.HashDistCompute(B, n, seedpath = tissue + "/seed.txt", gfolder=gfolder)
D_condensed = squareform(D)

hierarchy = linkage(D_condensed, method = method[tree_type])
cluster_list = hierarchy[:,:2].astype(int)
tree.TreeConstructor(cluster_list, n, B, gfolder = gfolder, outfolder = tissue + "/" + tree_type.upper())
