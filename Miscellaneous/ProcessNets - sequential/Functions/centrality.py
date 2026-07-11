# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 02:19:51 2025

@author: sugyani
"""

from Functions.envVar import setThreads
setThreads()

import warnings
warnings.filterwarnings("ignore")

import numpy as np

# %% Degree Centrality -- General (Static) Graphs
def DegreeCentrality(edges, n, average = False):
    '''
    This function computes the Degree Centrality of every node in a network.

    Parameters
    ----------
    edges : numpy ndarray or pandas DataFrame of dimensions m x 2.
        Each row is an edge of the co-expression network.
    n : int
        Number of nodes in the network.
    average : bool, optional
        If True, computes the average degree of the nodes, else returns the degree of every node. 
        The default is False.

    Returns
    -------
    deg: 1-D numpy array of size n
        Every element is the degree centrality of the node representing the corresponding index.
    '''
    
    deg = np.zeros(shape = (n,), dtype = np.int16)
    for e in edges:
        deg[e[0]] += 1
        deg[e[1]] += 1
    
    #data_tab = np.unique(edges, return_counts=True)
    #deg = np.zeros(shape = (n,), dtype = np.int16)
    #deg[data_tab[0]] = data_tab[1]
    if average:
        return deg / n
    return deg

def DyDegreeCentrality(deg_t, edges_delta, n, average = False):
    deg_t1 = deg_t.copy()
    for e in edges_delta:
        deg_t1[e[0]] += 1
        deg_t1[e[1]] += 1
    
    #data_tab = np.unique(edges_delta, return_counts=True)
    #deg_t1[data_tab[0]] += data_tab[1]
    if average:
        return deg_t1 / n
    return deg_t1

# %% PageRank Centrality
from scipy.sparse.linalg import minres, spsolve
   
def ComputeDTilde(D):
    D1 = D.copy()
    D1[D1==0] = 1
    return D1

def PageRankCentrality(A, D, alpha=0.85, beta=0.15):
    D_tilde = ComputeDTilde(D)
    b = beta * np.ones(shape=D_tilde.shape)
    M = (-alpha) * A
    M.setdiag(D_tilde)
    y, _ = minres(M, b, x0 = None)
    #y = spsolve(M, b)    
    return M, y

def DyPageRankCentrality(M_t, D_t, y_t, A_delta, D_delta, alpha=0.85):    
    D_t1 = D_t + D_delta
    
    D_t_tilde = ComputeDTilde(D_t)
    D_t1_tilde = ComputeDTilde(D_t1)
    M_delta = (-alpha) * A_delta
    M_delta.setdiag(D_t1_tilde - D_t_tilde)
    
    M_t1 = M_t + M_delta
    y_delta, _ = minres(M_t1, M_delta @ y_t, x0 = y_t)
    #y_delta = spsolve(M_t1, M_delta @ y_t)
    return M_t1, D_t1, y_t-y_delta, D_t1_tilde

