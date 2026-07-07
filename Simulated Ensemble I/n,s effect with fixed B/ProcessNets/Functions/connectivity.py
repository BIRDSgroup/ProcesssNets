# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 16:07:02 2025

@author: HP
"""

from Functions.envVar import setThreads
setThreads()

from collections import defaultdict

# %% DSU DS
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.size = [1] * size
        self.compSize = []

    def find(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])        
        return self.parent[x]

    def union(self, a, b):
        rootA = self.find(a)
        rootB = self.find(b)
        
        if self.size[rootA] < self.size[rootB]:
            self.parent[rootA] = rootB
            self.size[rootB] += self.size[rootA]
        else:
            self.parent[rootB] = rootA
            self.size[rootA] += self.size[rootB]
            
    def connected(self, a, b):
        return self.find(a) == self.find(b)
    
    def copy(self):
        new = UnionFind(len(self.parent))
        new.parent = self.parent.copy()
        new.size = self.size.copy()
        new.compSize = self.compSize.copy()
        return new
    
    def getSizes(self):
        self.compSize = []
        for v in range(len(self.parent)):
            self.compSize.append(self.size[self.find(v)])
    
    def getComponents(self):
        components = defaultdict(set)
        for idx in range(len(self.parent)):
            root = self.find(idx)
            components[root].add(idx)
        return list(dict(components).values())
        
# %% Connected Components -- Static Graphs
def CComponents(edges, n):
    graph = UnionFind(n)
    check = False
    for e in edges:
        #e = edges.loc[idx,:]
        if not graph.connected(e[0], e[1]):
            graph.union(e[0], e[1])
            check = True
    if check:
        graph.getSizes()
    return graph
    
# %% Connected Components -- Incremental Graphs
def DyCComponents(graph_t, edges_delta, n):
    graph_t1 = graph_t.copy()
    check = False
    for e in edges_delta:
        #e = edges_delta.loc[idx,:]
        if not graph_t1.connected(e[0], e[1]):
            graph_t1.union(e[0], e[1])
            check = True    
    if check:
        graph_t1.getSizes()
    return graph_t1
    