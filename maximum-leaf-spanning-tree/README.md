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

-   `problem01.lp`: 51.829s.
-   `problem02.lp`: 67.895s.
-   `problem03.lp`: 111.803s.
-   `problem04.lp`: 202.521s.
-   `problem05.lp`: 288.372s.
-   `problem06.lp`: 8.369s.
-   `problem07.lp`: 41.712s.
-   `problem08.lp`: 175.536s.
-   `problem09.lp`: 127.363s.
-   `problem10.lp`: 268.736s.
