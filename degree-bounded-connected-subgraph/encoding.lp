{ in(E) } :- edge(E).

% A graph is connected if every vertex is reachable from every other vertex.
r(X, Y) :- in(E), e(E, X), e(E, Y), X < Y.
r(X, Z) :- X < Z, Y < X, r(Y, X), e(E, Y), e(E, Z), in(E).
r(X, Z) :- X < Z, Y > X, r(X, Y), e(E, Y), e(E, Z), in(E).

:- vtx(X), vtx(Y), X < Y, not r(X, Y).

% Check that the degree limit is not exceeded:
:- #count{ E : in(E), e(E, X), e(E, Y) } > D, vtx(X), degree(D).

:~ edge(E), not in(E). [1@1, E]
