{in(X)} :- c(X, N).
:- s(N), #count{X : in(X), c(X, N)} = 0.
:~ in(X). [1@1, X]
