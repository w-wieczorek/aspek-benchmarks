{ selected(I, O) : input(I), output(O) }.

% Obliczanie os. U -> V
reachable(U, V) :- edge(U, V).
reachable(U, W) :- reachable(U, V), edge(V, W).

covered_by(V, I, O) :-
    vertex(V),
    selected(I, O),
    reachable(I, V),
    reachable(V, O).

covered_by(I, I, O) :- selected(I, O), input(I).
covered_by(O, I, O) :- selected(I, O), output(O).

covered(V) :- covered_by(V, _, _).
:- vertex(V), not covered(V).

% Minimalizacja liczby testow
:~ selected(I, O). [1@1, I, O]
