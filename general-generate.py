import networkx as nx
import random
from scipy.io import mmwrite
from functools import reduce
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Data generation tool for the near-clique problem.")
parser.add_argument('--n', type=int, help="Number of vertices", default=20)
parser.add_argument('--m', type=int, help="Number of edges", default=70)
parser.add_argument('--f', type=str, help="Name of the output file", default="graph")
args = parser.parse_args()

n, m = args.n, args.m

# Generate a random seed and graph
seed = random.randint(1, 4000000000)
repeat = True
while repeat:
  seed = random.randint(1, 4000000000)
  print(f"seed = {seed}")
  graph = nx.gnm_random_graph(n, m, seed, directed=False)
  repeat = not nx.is_connected(graph)

for u, v in graph.edges():
  graph[u][v]['weight'] = random.randint(1, 50)

#graph = nx.barabasi_albert_graph(n, m, seed)
#graph = nx.expected_degree_graph(reduce(lambda l1, l2: l1 + l2, ([i]*i for i in range(3, 23))), selfloops=False, seed=seed)
#graph = nx.ring_of_cliques(n, m)
#graph = nx.ladder_graph(n)

with open(f"{args.f}_{n}_{m}.lp", "w") as f:
    f.write(f"vtx(1..{len(graph.nodes)}).\n")
    # f.write(f"root({random.randint(1, n)}).\n")
    f.write(f"edge(1..{len(graph.edges)}).\n")
    # f.write(f"degree(4).\n")
    # for v in graph.nodes:
    #     f.write(f"r({v+1}, {random.randint(1, 3)}).\n")
    #i = 0
    for (u, v) in graph.edges:
        # i += 1
        # f.write(f"e({i},{u + 1}).\n")
        # f.write(f"e({i},{v + 1}).\n")
        # if u < v:
        #    f.write(f"edge({u+1}, {v+1}).\n")
        #    f.write(f"len({u+1}, {v+1}, {random.randint(1, 100)}).\n")
        #    f.write(f"c({u+1}, {v+1}, {random.randint(5, 20)}).\n")
        # else:
        #    f.write(f"edge({v+1}, {u+1}).\n")
        #    f.write(f"len({v+1}, {u+1}, {random.randint(1, 100)}).\n")
        #    f.write(f"c({v+1}, {u+1}, {random.randint(1, 10)}).\n")
        f.write(f"edge({u+1}, {v+1}, {graph[u][v]['weight']}).\n")
#    for u in graph.nodes:
#      for v in graph.nodes:
#        if u < v and (u, v) not in graph.edges:
#          f.write(f":- v_in({u + 1}), v_in({v + 1}).\n")
# 
# with open(f"{args.f}_{n}_{m}.wcnf", "w") as f:
#     for r in range(2, n + 1):
#         for s in range(1, r):
#             for u in range(2, n + 1):
#                 for v in range(1, u):
#                     if ((r, s) < (u, v)) and ((s-1, r-1) not in graph.edges) and ((v-1, u-1) not in graph.edges):
#                         f.write(f"h -{r} -{s} -{u} -{v} 0\n")
#     for i in range(1, n + 1):
#         f.write(f"1 {i} 0\n")
# 
# adj_matrix1 = nx.to_numpy_array(graph, dtype=int)
# 
# with open(f"{args.f}_{n}_{m}.txt", "w") as f:
#     for row in adj_matrix1:
#         line = ''.join(map(str, row))  # Konwersja wiersza na ciąg znaków bez spacji
#         f.write(line + '\n')

print(f"A graph written to a file with seed: {seed}")
