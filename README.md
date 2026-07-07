# PROperty Computation in EnSembleS of NETworkS ($\texttt{ProcessNets}$)
This repository contains scripts for implementation of the $\texttt{ProcessNets}$ framework to compute four network science measures, namely, degree centrality, component size, PageRank (PR) centrality, and closeness centrality, in an ensemble of networks. Details regarding this workflow, a related $\texttt{nc}$-tree, and associated data and results are explained in detail in the following manuscript. 

- [insert citation here]

## Overview of the Project
Given an ensemble of undirected unweighted networks, each defined on the same set of nodes, but with different edge sets, this project develops a systematic and versatile framework to efficiently compute different local/global network science measures in each of the networks.
The framework exploits the structural similarity among the networks to hierarchically organize them into a $\texttt{nc}$-tree and computes the a network science measure by repeatedly applying an incremental dynamic algorithm.
The current version of this project is implemented only for four network science measures, namely, degree centrality, component size, PageRank (PR) centrality, and closeness centrality and for five configurations of the framework and two configurations of the baseline approach.

The five configurations of the framework is designed to run on $5$ cores, wherein one core is designated for each configuration.
However, we also provide the code for sequential execution of all configurations.
If only a subset of these seven configurations need to be executed, then the corresponding codes can also be easily modified.
It may be noted here that the current version of the project supports only undirected and unweighted networks as the static graph and incremental dynamic graph algorithms are implemented accordingly, and can be easily modified to support other variants of networks by modifying the graph algorithms.

The project is implemented using the following programming languages: 

-  *Preprocessing of real-world datasets*: R version 4.4.2
-  *Functions for computations and analyses*: Python versions 3.10 and 3.12. 
   Packages like `numpy, pandas, scipy, random, corals.correlation` and `statsmodel` have been used repeatedly.
-  *Workflows combining several scripts*: Bourne Again SHell (BASH) scripting language

### Getting Started

This section will help you set up the project for the first time — from cloning the repository to running a complete example. 
Please follow each step in the given order.

1. **Clone/download the project from GitHub to your local machine.**
```bash
git clone https://github.com/BIRDSgroup/ProcesssNets PNets
cd PNets
```
If you want to run all five framework configurations on five cores with each configuration on a dedicated core, then please use:
```bash
cd "ProcessNets"
```
Else if you want to run each configuration sequentially, then please use:
```bash
cd "ProcessNets - sequential"
```
2. **Prepare input data.**
   
As previously mentioned, this framework takes as input an ensemble of networks.
Suppose your ensemble is titled `Ensemble`.
Then please create a folder titled `graphs_Ensemble`, and store your networks inside this folder.
Each network $G_i$ should be stored in the file `i.csv` and should contain the edge list of the i<sup>th</sup> network - each row representing an edge in the network.

For example, using the Python programming language, if the `A` variable stores the adjacency matrix of the i<sup>th</sup> network, then you may use:
```python
import numpy as np
edges = np.argwhere(A)
np.savetxt('graphs_Ensemble/' + str(i) + '.csv', edges, delimiter=',', fmt='%d')
```
Similarly, if your i<sup>th</sup> network $G_i$ is constructed using the `networkx` Python package and represented using the variable `Gi`, then please use: 
```python
import numpy as np
import networkx as nx
#edges = list(Gi.edges()) # required only if you want to generate the list of edges
nx.write_edgelist(Gi, 'graphs_Ensemble/' + str(i) + '.csv', delimiter=",", data=False)
```
3. **Choosing which configurations to run** - [optional]
The current version of the framework constructs five $\texttt{nc}$-trees, namely, $\mathrm{rstar}$, $\mathrm{slink}$, $\mathrm{fpa}$, $\mathrm{upgma}$, and $\mathrm{wpgmc}$, and computes three network science measures, namely, degree centrality, component size, and PR centrality, using each of these five $\texttt{nc}$-trees and two versions of the baseline approach -- a self-implementation and using the `networkx` package.
If you are not interested to run any of these configurations, then please use any text editor to edit `main.sh` as follows:
