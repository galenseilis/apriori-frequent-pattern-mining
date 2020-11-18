import networkx as nx
from itertools import combinations
from apriori import scan_db
import matplotlib.pyplot as plt
from graphviz import Graph

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




G = from_tfile('data.txt')

g = Graph('multi')
for edge in G.edges():
    g.edge(str(edge[0]), str(edge[1]))
g.view()

g = Graph('single')
for edge in set(G.edges()):
    g.edge(str(edge[0]), str(edge[1]))
g.view()
