# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 03:59:50 2025

@author: HP
"""

from Functions.envVar import setThreads
setThreads()

# %% Packages
import numpy as np
import pandas as pd

# %% Degree Centrality
def TreeDegree(folder, B, n, out_file, nonbinary=False):
    from Functions import centrality
    DF = pd.Series()
    
    # %%% Root Graph
    root = 2*(B-1)
    if nonbinary:
        child_count = pd.read_csv(folder + 'child_count.tsv', header=None, index_col=0, sep='\t')[1]
        root = max(child_count.index)
    
    edges_root = np.genfromtxt(folder + 'root.csv', delimiter=',', dtype=int)
    DF[root] = centrality.DegreeCentrality(edges_root, n)
    
    # %%% THE TREE
    tree_data = pd.read_csv(folder + 'info.tsv', header=None, index_col=0, sep='\t')
    count = np.zeros(shape=(root+1,), dtype=np.int16)    
    for idx in tree_data.index[::-1]:        
        pnode = tree_data.loc[idx, 1]
        cnode = tree_data.loc[idx, 2]
        
        if tree_data.loc[idx,3]:
            terminal_delta = pd.read_csv(folder + str(idx) + '.csv', header=None, index_col=None, sep=',', dtype=int)[0]
            edges_delta = np.zeros(shape=(len(terminal_delta), 2), dtype=int)
            edges_delta[:,0] = terminal_delta // n
            edges_delta[:,1] = terminal_delta % n            
            DF[cnode] = centrality.DyDegreeCentrality(DF[pnode], edges_delta, n)
        else:
            DF[cnode] = DF[pnode].copy()
            
        count[pnode] += 1
        if count[pnode] == (child_count[pnode] if nonbinary else 2):
            DF = DF.drop(index=pnode)
        if cnode < B:
            with open(out_file, 'a') as op_file:
                print(cnode, *DF[cnode], sep=',', end='\n', file=op_file)
            op_file.close()
            DF = DF.drop(index=cnode)
    return

# %% Connected Components
def TreeConnectivity(folder, B, n, out_file, nonbinary=False):
    from Functions import connectivity
    DF = pd.Series()
    
    # %%% Root Graph
    root = 2*(B-1)
    if nonbinary:
        child_count = pd.read_csv(folder + 'child_count.tsv', header=None, index_col=0, sep='\t')[1]
        root = max(child_count.index)
    
    edges_root = np.genfromtxt(folder + 'root.csv', delimiter=',', dtype=int)
    DF[root] = connectivity.CComponents(edges_root, n)
    
    # %%% THE TREE
    tree_data = pd.read_csv(folder + 'info.tsv', header=None, index_col=0, sep='\t')
    count = np.zeros(shape=(root+1,), dtype=np.int16)
    for idx in tree_data.index[::-1]:
        pnode = tree_data.loc[idx, 1]
        cnode = tree_data.loc[idx, 2]
        
        if tree_data.loc[idx,3]:
            terminal_delta = pd.read_csv(folder + str(idx) + '.csv', header=None, index_col=None, sep=',', dtype=int)[0]
            edges_delta = np.zeros(shape=(len(terminal_delta), 2), dtype=int)
            edges_delta[:,0] = terminal_delta // n
            edges_delta[:,1] = terminal_delta % n
            #edges_delta = pd.DataFrame(edges_delta)
            
            graph_ds = connectivity.DyCComponents(DF[pnode], edges_delta, n)
        else:
            graph_ds = DF[pnode].copy()
        
        if cnode < B:
            with open(out_file, 'a') as op_file:
                print(cnode, *graph_ds.compSize, sep=',', end='\n', file=op_file)
            op_file.close()
        else:
            DF[cnode] = graph_ds.copy()
        del graph_ds
                
        count[pnode] += 1
        if count[pnode] == (child_count[pnode] if nonbinary else 2):
            DF = DF.drop(index=pnode)
    return

# %% Closeness Centrality
def TreeCloseness(folder, B, n, out_file, nonbinary=False):
    import networkx as nx
    from networkx.algorithms import closeness_centrality as CC
    from networkx.algorithms import incremental_closeness_centrality as incCC
    
    DF = pd.DataFrame(columns = ['G', 'cc'])
    
    # %%% Root Graph
    root = 2*(B-1)
    if nonbinary:
        child_count = pd.read_csv(folder + 'child_count.tsv', header=None, index_col=0, sep='\t')[1]
        root = max(child_count.index)
    
    edges_root = np.genfromtxt(folder + 'root.csv', delimiter=',', dtype=int)
    G_root = nx.from_edgelist(edges_root)
    G_root.add_nodes_from(range(n))
    DF.loc[root, :] = [G_root, CC(G_root)]
    del G_root
    
    # %%% THE TREE
    tree_data = pd.read_csv(folder + 'info.tsv', header=None, index_col=0, sep='\t')
    count = np.zeros(shape=(root+1,), dtype=np.int16)
    for idx in tree_data.index[::-1]:
        pnode = tree_data.loc[idx, 1]
        cnode = tree_data.loc[idx, 2]
        
        G = DF.loc[pnode, 'G'].copy()
        cc = DF.loc[pnode, 'cc'].copy()
        
        if tree_data.loc[idx,3]:
            terminal_delta = pd.read_csv(folder + str(idx) + '.csv', header=None, index_col=None, sep=',', dtype=int)[0]
            edges_delta = np.zeros(shape=(len(terminal_delta), 2), dtype=int)
            edges_delta[:,0] = terminal_delta // n
            edges_delta[:,1] = terminal_delta % n
            #edges_delta = pd.DataFrame(edges_delta)
            
            for edge in edges_delta:
                cc = incCC(G, edge, prev_cc=cc, insertion=True)
                G.add_edge(*edge)
                
        if cnode < B:
            cc_sorted = [0]*n
            for k in range(n):
                cc_sorted[k] = cc[k]
            with open(out_file, 'a') as op_file:
                print(cnode, *cc_sorted, sep=',', end='\n', file=op_file)
            op_file.close()
        else:
            DF.loc[cnode,:] = [G, cc]
        del G, cc
        
        count[pnode] += 1
        if count[pnode] == (child_count[pnode] if nonbinary else 2):
            DF = DF.drop(index=pnode)
    return

# %% PageRank Centrality
def TreePageRank(folder, B, n, out_file, nonbinary=False):
    from Functions import centrality
    from scipy.sparse import csr_array
    
    DF = pd.DataFrame(columns=['M', 'D', 'y'])
    
    # %%% Root Graph
    root = 2*(B-1)
    if nonbinary:
        child_count = pd.read_csv(folder + 'child_count.tsv', header=None, index_col=0, sep='\t')[1]
        root = max(child_count.index)
    
    edges_root = np.genfromtxt(folder + 'root.csv', delimiter=',', dtype=int)
    A_root = np.zeros(shape=(n,n), dtype=int)
    if edges_root.size != 0:
        A_root[edges_root[:,0], edges_root[:,1]] = A_root[edges_root[:,1], edges_root[:,0]] = 1    
    D_root = np.sum(A_root, axis=0)
    
    M_root, y_root = centrality.PageRankCentrality(csr_array(A_root), D_root)
    
    DF.loc[root, :] = [M_root, D_root, y_root]
    del A_root, M_root, D_root, y_root
    
    # %%% THE TREE
    tree_data = pd.read_csv(folder + 'info.tsv', header=None, index_col=0, sep='\t')
    count = np.zeros(shape=(root+1,), dtype=np.int16)
    for idx in tree_data.index[::-1]:
        pnode = tree_data.loc[idx, 1]
        cnode = tree_data.loc[idx, 2]
                
        if tree_data.loc[idx,3]:
            terminal_delta = pd.read_csv(folder + str(idx) + '.csv', header=None, index_col=None, sep=',', dtype=int)[0]
            edges_delta = np.zeros(shape=(len(terminal_delta), 2), dtype=int)
            edges_delta[:,0] = terminal_delta // n
            edges_delta[:,1] = terminal_delta % n
            #edges_delta = pd.DataFrame(edges_delta)
            
            A_delta = np.zeros(shape=(n,n), dtype=int)
            A_delta[edges_delta[:,0], edges_delta[:,1]] = A_delta[edges_delta[:,1], edges_delta[:,0]] = 1
            D_delta = np.sum(A_delta, axis=0)
                        
            M_t1, D_t1, y_t1, D_t1_tilde = centrality.DyPageRankCentrality(DF.loc[pnode, 'M'], DF.loc[pnode, 'D'], DF.loc[pnode, 'y'], csr_array(A_delta), D_delta)
            
        else:
            M_t1, D_t1, y_t1 = DF.loc[pnode,:].values
            D_t1_tilde = centrality.ComputeDTilde(D_t1)
            
                            
        if cnode < B:
            pr = D_t1_tilde * y_t1    
            with open(out_file, 'a') as op_file:
                print(cnode, *pr, sep=',', end='\n', file=op_file)
            op_file.close()
        else:
            DF.loc[cnode,:] = [M_t1, D_t1, y_t1]
        
        count[pnode] += 1
        if count[pnode] == (child_count[pnode] if nonbinary else 2):
            DF = DF.drop(index=pnode)
    return
    

# %% k-core decomposition -- core number
def TreeCoreDecomposition(folder, B, n, out_file, nonbinary=False):
    from Functions import cores
    DF = pd.DataFrame(columns = ['G', 'core'])
    
    # %%% Root Graph
    root = 2*(B-1)
    if nonbinary:
        child_count = pd.read_csv(folder + 'child_count.tsv', header=None, index_col=0, sep='\t')[1]
        root = max(child_count.index)
    
    edges_root = pd.read_csv(folder + 'root.csv', header=None, index_col=None, sep=',', dtype=int)
    
    G_root = {i: set() for i in range(n)}
    for i in edges_root.index:
        edge = edges_root.loc[i,:].values
        G_root[edge[0]].add(edge[1])
        G_root[edge[1]].add(edge[0])
    DF.loc[root, :] = [G_root, cores.CoreNumber(G_root, n)]
    del G_root
    
    # %%% THE TREE
    tree_data = pd.read_csv(folder + 'info.tsv', header=None, index_col=0, sep='\t')
    count = np.zeros(shape=(root+1,), dtype=np.int16)
    for idx in tree_data.index[::-1]:
        pnode = tree_data.loc[idx, 1]
        cnode = tree_data.loc[idx, 2]
        
        if tree_data.loc[idx,3]:
            terminal_delta = pd.read_csv(folder + str(idx) + '.csv', header=None, index_col=None, sep=',', dtype=int)[0]
            edges_delta = np.zeros(shape=(len(terminal_delta), 2), dtype=int)
            edges_delta[:,0] = terminal_delta // n
            edges_delta[:,1] = terminal_delta % n
            edges_delta = pd.DataFrame(edges_delta)            
            DF.loc[cnode,:] = cores.DyCoreNumber(DF.loc[pnode,'G'], DF.loc[pnode,'core'], edges_delta, n)
        else:
            DF.loc[cnode,:] = DF.loc[pnode,:].copy()
            
        count[pnode] += 1
        if count[pnode] == (child_count[pnode] if nonbinary else 2):
            DF = DF.drop(index=pnode)
        if cnode < B:
            with open(out_file, 'a') as op_file:
                print(cnode, *DF.loc[cnode,'core'], sep=',', end='\n', file=op_file)
            op_file.close()
            DF = DF.drop(index=cnode)
    return
