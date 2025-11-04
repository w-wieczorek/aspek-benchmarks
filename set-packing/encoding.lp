{in(X)} :- subset(X).
:- in(X), in(Y), X != Y, c(X, E), c(Y, E).
:~ subset(X), not in(X). [1@1, X]