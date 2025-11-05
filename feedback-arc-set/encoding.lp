{ remove(U, V) } :- arc(U, V).
remaining(U, V) :- arc(U, V), not remove(U, V).

reachable(U, V) :- remaining(U, V).
reachable(U, W) :- reachable(U, V), remaining(V, W).

:- reachable(V, V), vtx(V).

:~ remove(U, V). [1@1, U, V]

