import networkx as nx
import random

def generate_cubic_hard_instance(n, seed):
    if n % 2 != 0:
        n += 1  # Must be even
    G = nx.random_regular_graph(3, n, seed=seed)
    if not nx.is_connected(G):
        print(f"Graph is not connected for seed {seed} !!!")
    return G

def generate_min_degree_instance(n, seed, min_deg=3, avg_deg=5):
    m = int(n * avg_deg / 2)
    G = nx.gnm_random_graph(n, m, seed=seed)
    random.seed(seed)
    while not nx.is_connected(G) or min(dict(G.degree()).values()) < min_deg:
        seed += 1
        G = nx.gnm_random_graph(n, m, seed=seed)
        for v in G.nodes():
            while G.degree(v) < min_deg:
                u = random.choice([x for x in G.nodes() if x != v and not G.has_edge(v, x)])
                G.add_edge(v, u)
    if not nx.is_connected(G):
        print(f"Graph is not connected for seed {seed} !!!")
    return G

seeds = [
    (35, 4210067), (36, 1662988), (38, 3086742), (40, 9491513), (40, 5655004),
    (60, 263067), (65, 3454786), (66, 2169901), (67, 7187272), (71, 2987890),
]

for i, (size, seed) in enumerate(seeds):
    if i < 5:
        G = generate_cubic_hard_instance(size, seed)
    else:
        G = generate_min_degree_instance(size, seed)
    n_nodes = G.number_of_nodes()
    with open(f"problem{i+1:02d}.lp", "w") as f:
        f.write(f"node(0..{n_nodes-1}).\n")
        for u, v in G.edges():
            f.write(f"edge({u}, {v}).\n")
