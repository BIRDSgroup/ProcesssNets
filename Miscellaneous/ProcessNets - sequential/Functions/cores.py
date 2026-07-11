# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 21:08:23 2025

@author: HP
"""
from Functions.envVar import setThreads
setThreads()

# %% Core Number -- Static Graphs
def CoreNumber(G, n):
    degrees = {v:len(G[v]) for v in range(n)}
    nodes = sorted(degrees, key=degrees.get)
    bin_boundaries = [0]
    curr_degree = 0
    for i, v in enumerate(nodes):
        if degrees[v] > curr_degree:
            bin_boundaries.extend([i] * (degrees[v] - curr_degree))
            curr_degree = degrees[v]
    node_pos = {v: pos for pos, v in enumerate(nodes)}
    # The initial guess for the core number of a node is its degree.
    core = {v:degrees[v] for v in degrees}
    nbrs = {v:G[v].copy() for v in G}
    for v in nodes:
        for u in nbrs[v]:
            if core[u] > core[v]:
                nbrs[u].remove(v)
                pos = node_pos[u]
                bin_start = bin_boundaries[core[u]]
                node_pos[u] = bin_start
                node_pos[nodes[bin_start]] = pos
                nodes[bin_start], nodes[pos] = nodes[pos], nodes[bin_start]
                bin_boundaries[core[u]] += 1
                core[u] -= 1    
    return list(core.values())

# %% Core Number -- Dynamic Incremental Graphs
from collections import deque
def __induced_subgraph(graph, nodes_set):
    return {v: set(u for u in graph[v] if u in nodes_set) for v in nodes_set}

def __subcore(graph_sub):    
    nodes = list(graph_sub.keys())
    idx = {v:i for i,v in enumerate(nodes)}
    inv = {i:v for v,i in idx.items()}
    g_mapped = {i: set(idx[u] for u in graph_sub[inv[i]]) for i in range(len(nodes))}
    core_mapped = CoreNumber(g_mapped, len(nodes))
    return {inv[i]: core_mapped[i] for i in range(len(nodes))}

def DyCoreNumber(G_t, core_t, edges_delta, n):  
    G_t1 = {v: G_t[v].copy() for v in G_t}
    core_t1 = core_t.copy()
    
    # Insert edges into graph    
    for idx in edges_delta.index:
        u, v = edges_delta.loc[idx,:].values.tolist()
        G_t1[u].add(v)
        G_t1[v].add(u)
    
    # Candidates: nodes whose degree now exceeds their core
    candidates = set()
    for idx in edges_delta.index:
        u, v = edges_delta.loc[idx,:].values.tolist()
        if len(G_t1[u]) > core_t1[u]:
            candidates.add(u)
        if len(G_t1[v]) > core_t1[v]:
            candidates.add(v)
    if not candidates:
        return G_t1, core_t1
    
    # build affected region L by BFS from candidates, traversing nodes with core >= c_min
    c_min = min(core_t1[v] for v in candidates)    
    L = set()
    Q = deque(candidates)
    visited = set(candidates)
    while Q:
        v = Q.popleft()
        L.add(v)
        for u in G_t1[v]:
            if u not in visited and core_t1[u] >= c_min:
                visited.add(u)
                Q.append(u)
    
    # compute exact k-core on induced subgraph and update cores
    subG = __induced_subgraph(G_t1, L)
    core_sub = __subcore(subG)
    for v, newc in core_sub.items():
        if newc > core_t1[v]:
            core_t1[v] = newc
            
    return G_t1, core_t1
