# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 18:11:03 2025

@author: HP
"""

from Functions.envVar import setThreads
setThreads()

# %% Packages
import numpy as np
import pandas as pd
import os

# %% The Functions
def TreeConstructor(cluster_list, n, B, gfolder, outfolder):
    parent = B
    edge_counter = 1
    for cluster in cluster_list:
        terminals = dict()
        for idx, child in enumerate(cluster):
            if os.path.getsize('graphs_' + gfolder + '/' + str(child) + '.csv'):
                cedges = pd.read_csv('graphs_' + gfolder + '/' + str(child) + '.csv', header=None, index_col=None, sep=',', dtype=int)
                terminals[idx] = cedges[0]*n + cedges[1]
            else:
                terminals[idx] = pd.Series(dtype=int)
                    
        if len(terminals[0]) < len(terminals[1]):
            pterminal = terminals[0][terminals[0].isin(terminals[1])]
        else:
            pterminal = terminals[1][terminals[1].isin(terminals[0])]
        pedges = np.zeros(shape=(len(pterminal), 2), dtype=int)
        pedges[:,0] = pterminal // n
        pedges[:,1] = pterminal % n
        
        np.savetxt('graphs_' + gfolder + '/' + str(parent) + '.csv', pedges, delimiter=',', fmt='%d')
        
        for i in range(len(cluster)):
            tedge_terminal = terminals[i][~terminals[i].isin(pterminal)]
            #tedge_edges = np.zeros(shape=(len(tedge_terminal), 2), dtype=int)
            #tedge_edges[:,0] = tedge_terminal // n
            #tedge_edges[:,1] = tedge_terminal % n
            np.savetxt(outfolder + '/' + str(edge_counter + i) + '.csv', tedge_terminal, delimiter=',', fmt='%d')
            with open(outfolder + '/info.tsv', 'a') as info_file:
                print(edge_counter + i, parent, cluster[i], len(tedge_terminal), sep='\t', end='\n', file=info_file)
            info_file.close()
                    
        # Variables Update
        parent += 1
        edge_counter += len(cluster)
    return

def HashDistCompute(B, n, seedpath, gfolder, k=10):
    from numpy.random import permutation, seed
    import os
    
    if os.path.exists(seedpath):
        with open(seedpath, 'r') as seed_file:
            seed(int(seed_file.read()))
        
    m_max = np.triu_indices(n)
    m_max = m_max[0]*n + m_max[1]
    hash_vals = {b:[] for b in range(B)}    
    for i in range(k):
        order = permutation(m_max)
        for b in range(B):
            edges = pd.read_csv('graphs_' + gfolder + '/' + str(b) + '.csv', header=None, index_col=None, sep=',', dtype=int)
            terminal = edges[0]*n + edges[1]
            hash_vals[b].append(next(x for x in order if x in terminal.values))
    
    Dist = pd.DataFrame(0, index=range(B), columns=range(B))
    for b1 in range(B):
        for b2 in range(b1+1, B):
            Dist.loc[b1,b2] = Dist.loc[b2,b1] = np.sum(np.array(hash_vals[b1]) != np.array(hash_vals[b2]))       
    return Dist

def JSICompute(n, gfolder, ecfolder=None):
    n = int(n)
    if n == -1:
        ec = pd.read_csv(ecfolder + '/edge count.tsv', header=None, index_col=0, sep='\t')
        n = ec.loc[0, 1]
    
    JSI = pd.DataFrame(1.0, index=range(10), columns=range(10))
    for b1 in range(10):
        edges = pd.read_csv('graphs_' + gfolder + '/' + str(b1) + '.csv', header=None, index_col=None, sep=',', dtype=int)
        t1 = set(edges[0]*n + edges[1])
        for b2 in range(b1+1, 10):
            edges = pd.read_csv('graphs_' + gfolder + '/' + str(b2) + '.csv', header=None, index_col=None, sep=',', dtype=int)
            t2 = set(edges[0]*n + edges[1])
            
            cap = len(t1 & t2)
            cup = len(t1) + len(t2) - cap
            JSI.loc[b1,b2] = JSI.loc[b2,b1] =  cap / cup
    print('Mean JSI values = ', JSI.mean(axis=None))