{in(X)} :- vtx(X).
:- #count{N : edge(N), e(N, X), e(N, Y), in(X)} = 0, vtx(Y), not in(Y).
:~ in(X). [1@1, X]
