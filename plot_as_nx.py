import networkx as nx
from itertools import combinations
from apriori import scan_db
import matplotlib.pyplot as plt

def from_tfile(file):
    g = nx.MultiGraph()
    for (t_id, t_n, t_set) in scan_db(file):
        for comb in combinations(t_set, r=2):
            g.add_edge(comb[0], comb[1])
    return g

def count_cliques(G):
    c = 0
    for i in nx.algorithms.enumerate_all_cliques(G):
        c += 1
    return c




G = from_tfile('t25i10d10k.txt')
##count = 0
##for i, c in enumerate(nx.algorithms.find_cliques(G)):
##    count += 1
##    print(i, count, len(c))
files = ['data.txt',
         '1k5L.txt',
         't25i10d10k.txt',
         'retail.txt',
         'connect.txt']
for file in files:
    print(file)
    G = from_tfile(file)
    print(f'{nx.function.info(G)}')
    m = len(set(G.edges()))
    n = len(G.nodes())
    d = 2 * m / (n * (n - 1))
    print(f'Graph Density: {d}\n')
    
