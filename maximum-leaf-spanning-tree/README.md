# Maximum Leaf Spanning Tree (MLST)

-   Input: An undirected graph $G = (V, E)$.
-   Output: A spanning tree $T$ of $G$
-   Objective: Maximize $L(T) = \{v \in V : deg_T(v) = 1\}$, where $deg_T(v)$ denotes a degree of a vertex $v$ in $T$.
-   Feasibility Constraint: $T$ must span all vertices of $G$ and form a tree (connected and acyclic).

[ND2] in Garey & Johnson.

## Dataset

Instances are randomly generated with two scenarios:

-   random 3-regular graphs, which are APX-hard for MLST;
-   degree-constrained graphs with minimum degree >= 3.

## Time baseline

Measured with Clingo 5.6.2.

-   `p1.lp`: 51.829s.
-   `p2.lp`: 67.895s.
-   `p3.lp`: 111.803s.
-   `p4.lp`: 202.521s.
-   `p5.lp`: 288.372s.
-   `p6.lp`: 8.369s.
-   `p7.lp`: 41.712s.
-   `p8.lp`: 175.536s.
-   `p9.lp`: 127.363s.
-   `p10.lp`: 268.736s.
