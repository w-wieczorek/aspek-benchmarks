import networkx as nx
import random
import argparse

parser = argparse.ArgumentParser(description="Data generation tool for graphs.")
parser.add_argument('--n', type=int, help="Number of vertices")
parser.add_argument('--m', type=int, help="Number of all edges")
parser.add_argument('--d', type=int, help="Number of directed edges")
parser.add_argument('--f', type=str, help="Name of the output file")
args = parser.parse_args()

n, m, d = args.n, args.m, args.d

# Generate a random seed and graph
seed = random.randint(1, 4000000000)
repeat = True
while repeat:
    seed = random.randint(1, 4000000000)
    print(f"seed = {seed}")
    graph = nx.gnm_random_graph(n, m, seed, directed=False)
    repeat = not nx.is_connected(graph)

not_ok = True
directed = []
while not_ok:
    not_ok = False
    directed.clear()
    rs = random.sample(list(graph.edges), d)
    sources = set()
    targets = set()
    for (u, v) in rs:
        if random.randint(0, 1) == 1:
            if u in sources:
                not_ok = True
                break
            else:
                sources.add(u)
            if v in targets:
                not_ok = True
                break
            else:
                targets.add(v)
            directed.append((u, v))
        else:
            if v in sources:
                not_ok = True
                break
            else:
                sources.add(v)
            if u in targets:
                not_ok = True
                break
            else:
                targets.add(u)
            directed.append((v, u))


with open(f"{args.f}", "w") as f:
    f.write(f"vtx(1..{len(graph.nodes)}).\n")
    i = 0
    for (u, v) in graph.edges:
        # i += 1
        # f.write(f"e({i},{u + 1}).\n")
        # f.write(f"e({i},{v + 1}).\n")
        if (u, v) not in directed and (v, u) not in directed:
            if u < v:
                f.write(f"edge({u+1}, {v+1}).\n")
                f.write(f"len({u+1}, {v+1}, {random.randint(1, 100)}).\n")
            else:
                f.write(f"edge({v+1}, {u+1}).\n")
                f.write(f"len({v+1}, {u+1}, {random.randint(1, 100)}).\n")
        else:
            if (u, v) in directed:
                f.write(f"arc({u+1}, {v+1}).\n")
            else:
                f.write(f"arc({v+1}, {u+1}).\n")

print(f"A graph written to a file.")
