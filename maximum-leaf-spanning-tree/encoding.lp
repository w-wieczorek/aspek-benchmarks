{root(V) : node(V)} = 1.
% optionally: { parent_of(U,V); parent_of(V,U) } :- edge(U,V).
{parent_of(U, V)} :- edge(U, V).
{parent_of(U, V)} :- edge(V, U).
% excluding bi-directional parent-child relationships
:- edge(U, V), parent_of(U, V), parent_of(V, U).
% ensuring that the root has no parent
:- root(V), node(U), parent_of(U, V).
is_parent(U) :- parent_of(U, V).
% forbid any pair of distinct parents
:- parent_of(U, W), parent_of(V, W), U < V.
reachable(V) :- root(U), parent_of(U, V).
reachable(V) :- reachable(U), parent_of(U, V).
:- node(V), not root(V), not reachable(V).
:~ is_parent(V). [1@1, V]
