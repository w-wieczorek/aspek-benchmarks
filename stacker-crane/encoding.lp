{ starting_arc(U, V) : arc(U, V) } = 1.
{ in_cycle(U, V) } :- edge(U, V).
{ in_cycle(V, U) } :- edge(U, V).
:- edge(U, V), in_cycle(U, V), in_cycle(V, U).
in_cycle(U, V) :- arc(U, V).
reachable_from_start(V) :- starting_arc(U, V). 
reachable_from_start(V) :- reachable_from_start(W), in_cycle(W, V).
:- starting_arc(U, V), not reachable_from_start(U).
:- in_cycle(U1, V), in_cycle(U2, V), U1 != U2.
:- in_cycle(U, V1), in_cycle(U, V2), V1 != V2.
:~ edge(U, V), len(U, V, L), in_cycle(U, V). [L@1, U, V]
:~ edge(U, V), len(U, V, L), in_cycle(V, U). [L@1, U, V]

