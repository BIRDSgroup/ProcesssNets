# PROperty Computation in EnSembleS of NETworkS ($\texttt{ProcessNets}$)
This repository contains scripts for implementation of the $\texttt{ProcessNets}$ framework to compute four network science measures, namely, degree centrality, component size, PageRank (PR) centrality, and closeness centrality, in an ensemble of networks. Details regarding this workflow, a related $\texttt{nc}$-tree, and associated data and results are explained in detail in the following manuscript. 

- [insert citation here]

## Overview of the Project
Given an ensemble of undirected unweighted networks, each defined on the same set of nodes, but with different edge sets, this project develops a systematic and versatile framework to efficiently compute different local/global network science measures in each of the networks.
The framework exploits the structural similarity among the networks to hierarchically organize them into a $\texttt{nc}$-tree and computes a network science measure by repeatedly applying an incremental dynamic algorithm.
The current version of this project is implemented only for four network science measures, namely, degree centrality, component size, PageRank (PR) centrality, and closeness centrality and for five configurations of the framework and two configurations of the baseline approach.

The five configurations of the framework are designed to run on $5$ cores, wherein one core is designated for each configuration.
However, we also provide the code for sequential execution of all configurations.
If only a subset of these seven configurations needs to be executed, then the corresponding codes can also be easily modified.
It may be noted here that the current version of the project supports only undirected and unweighted networks as the static graph and incremental dynamic graph algorithms are implemented accordingly, and can be easily modified to support other variants of networks by modifying the graph algorithms.

The project is implemented using the following programming languages: 

-  *Preprocessing of real-world datasets*: R version 4.4.2
-  *Functions for computations and analyses*: Python versions 3.10 and 3.12. 
   Packages like `numpy, pandas, scipy, random, corals.correlation` and `statsmodel` have been used repeatedly.
-  *Workflows combining several scripts*: Bourne Again SHell (BASH) scripting language

## Getting Started

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
2. **Prepare input data.**<br>
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
<br>Similarly, if your i<sup>th</sup> network $G_i$ is constructed using the `networkx` Python package and represented using the variable `Gi`, then please use: 
```python
import numpy as np
import networkx as nx
#edges = list(Gi.edges()) # required only if you want to generate the list of edges
nx.write_edgelist(Gi, 'graphs_Ensemble/' + str(i) + '.csv', delimiter=",", data=False)
```
3. **Choosing which configurations to run** - [optional]<br>
The current version of the framework constructs five $\texttt{nc}$-trees, namely, $\mathrm{rstar}$, $\mathrm{slink}$, $\mathrm{fpa}$, $\mathrm{upgma}$, and $\mathrm{wpgmc}$, and computes three network science measures, namely, degree centrality, component size, and PR centrality, using each of these five $\texttt{nc}$-trees and two versions of the baseline approach -- a self-implementation and using the `networkx` package.
If you are not interested to run any of these configurations, then please use any text editor to edit `main.sh` as follows:
   1. If you don't want to construct $\mathrm{rstar}$, and do not want to compute the network science measures using the same, then please delete
      1. all occurrences of the word `rstar` from the file
      2. lines 22 to 25
   2. If you are not interested to construct any of the other $\texttt{nc}$-trees:<br>
   Suppose you don't want to construct $`\mathrm{tree} \in \{ \mathrm{slink}, \mathrm{fpa}, \mathrm{upgma}, \mathrm{wpgmc} \}`$, and hence do not want to compute the network science measures using $\mathrm{tree}$, then please delete all occurrences of the word `tree` from the file.
   3. If you want to construct $`\mathrm{tree} \in \{\mathrm{rstar}, \mathrm{slink}, \mathrm{fpa}, \mathrm{upgma}, \mathrm{wpgmc}\}`$, but you don't want to compute the network science measures using the same, then please delete the word `tree` from line 40.
   4. If you don't want to compute the network science measures using the baseline self-implementation, then please delete lines 57 -- 72.
   5. If you don't want to compute the network science measures using the baseline approach with `networkx` Python package, then please delete lines 74 -- 89.
   6. If you don't want to compute degree centrality, then please delete lines 42-43, 61-62, and 78-79.
   7. If you don't want to compute component size, then please delete lines 45-46, 64-65, and 81-82.
   8. If you don't want to compute PR centrality, then please delete lines 48-49, 67-68, and 84-85.
   9. If you want to compute closeness centrality using the framework configurations, then please uncomment lines 51-52.
   10. If you want to compute closeness centrality using the baseline approach with `networkx`, then please uncomment lines 87-88.
       
4. **Executing the Framework**<br>
Suppose your input ensemble has $B$ networks, each defined on $n$ nodes and generated from a dataset with $s$ samples. 
Let `Results` be the output folder to store all $\texttt{nc}$-trees, measurement values and other outputs. 
Then please run the following command from the terminal.
```bash
mkdir Results graphs_orig_Ensemble
time ./main.sh Results n B s Ensemble
```
If you don't have the information pertaining to the number of samples on which the networks are constructed, then please use the value $-1$ for $s$ i.e.,
```bash
mkdir Results graphs_orig_Ensemble
time ./main.sh Results n B -1 Ensemble
```

5. **Outputs**<br>
The framework output the folder `Results`, containing the following information:
   1. For each constructed $\texttt{nc}$-tree $`\mathrm{tree} \in \{\mathrm{rstar}, \mathrm{slink}, \mathrm{fpa}, \mathrm{upgma}, \mathrm{wpgmc}\}`$, a folder, titled `TREE` containing the following files.
      1. A file corresponding to each branch of the tree, containing the list of incremental edges along the same branch. These incremental edges are stored in the row-major flattened index, i.e., the edge $e = \{i,j\}$ between nodes $i$ and $j$ are stored as $i \times n + j$.
      2. `root.csv` - a file containing the edge list of the root network
      3. `info.tsv` - a tab-separated file containing the branch id, source network id, destination network id, and number of incremental edges along the branch.
      4. `child_count.tsv` - this file is generated only for the tree constructed using $`\mathrm{rstar}`$ and contains the number of children of each branching point.<br>
For example, consider the branch $(G_I, G_J)$ from $G_I$ to $G_J$ with the id $x$. The list of incremental edges along this branch, i.e., $E(G_J) \setminus E(G_I)$ is stored in the file `x.csv`. Suppose $|E(G_J) \setminus E(G_I)| = y$. Then, the $x$<sup>th</sup> line in `info.tsv` stores `x \t I \t J \t y`.
   2. `edge count.tsv` - a tab-separated file containing the number of nodes and number of edges of each network in the input ensemble
   3. `error.txt` - stores the total running time taken by the framework and errors, if any.
   4. `output.txt` - stores terminal outputs, if any.
   5. `jsi.txt` - stores the $\mathtt{MPJS}$ value of the ensemble.
   6. If degree centrality is computed, then: 
      1. For each $`\mathtt{ProcessNets}`$ configuration, $`\mathrm{config}`$, that is executed, a file titled `config degree.csv`.
      2. For the baseline approach with self-implementation, if executed, a file titled `mytrivial degree.csv`.
      3. For the baseline approach using `networkx` package, if executed, a file titled `trivial degree.csv`.
   7. If component size is computed, then: 
      1. For each $`\mathtt{ProcessNets}`$ configuration, $`\mathrm{config}`$, that is executed, a file titled `config connectivity.csv`.
      2. For the baseline approach with self-implementation, if executed, a file titled `mytrivial connectivity.csv`.
      3. For the baseline approach using `networkx` package, if executed, a file titled `trivial connectivity.csv`.
   8. If PR centrality is computed, then: 
      1. For each $`\mathtt{ProcessNets}`$ configuration, $`\mathrm{config}`$, that is executed, a file titled `config pr.csv`.
      2. For the baseline approach with self-implementation, if executed, a file titled `mytrivial pr.csv`.
      3. For the baseline approach using `networkx` package, if executed, a file titled `trivial pr.csv`.
   9. Running times are stored in the following files: 
      1. For each $`\mathtt{ProcessNets}`$ configuration, $`\mathrm{config}`$, that is executed, a file titled `config.txt`.
      2. For the baseline approach with self-implementation, if executed, a file titled `mytrivial.txt`.
      3. For the baseline approach using `networkx` package, if executed, a file titled `trivial.txt`.

## Replication of Results
For each dataset, we provide codes both for parallel and sequential execution of different ensembles, constructed using the same procedure on the respective datasets but with different values of the parameters. 
Note that, for parallel execution, each ensemble runs on dedicated $5$ cores and at most $10$ ensembles are run at a time, implying that, a minimum of $50$ cores is required for the parallel executions.

Before replicating the results, we start with cloning/downloading the project from GitHub to your local machine.
```bash
git clone https://github.com/BIRDSgroup/ProcesssNets PNets
cd PNets
```

- To replicate the results in Simulated Ensemble I, use:
```bash
cd "Simulated Ensemble I"
```
- To replicate the results in Simulated Ensemble II, use:
```bash
cd "Simulated Ensemble II"
```
- To replicate the results in Real-World Ensembles on variants from the Muscle Skeletal tissue, use:
```bash
cd "Real World Ensembles"/"Muscle Skeletal"
```
- To replicate the results in Real-World Ensembles on all chosen tissues, use:
```bash
cd "Real World Ensembles"/"All Chosen Tissues"
```

For executing the programs and replicating the results, please do the following:

If you want parallel execution:
```bash
time ./run_parallel.sh
```
If you want sequential execution:
```bash
time ./run_seq.sh
```
