vertex(1..100).

edge(1, 90).
edge(2, 92).
edge(2, 78).
edge(3, 26).
edge(3, 75).
edge(3, 45).
edge(4, 30).
edge(4, 39).
edge(4, 79).
edge(4, 92).
edge(5, 48).
edge(6, 57).
edge(7, 37).
edge(7, 57).
edge(8, 85).
edge(8, 31).
edge(9, 61).
edge(10, 49).
edge(10, 81).
edge(11, 10).
edge(11, 33).
edge(11, 62).
edge(11, 88).
edge(12, 6).
edge(13, 1).
edge(13, 95).
edge(13, 96).
edge(15, 72).
edge(16, 6).
edge(16, 17).
edge(16, 20).
edge(16, 41).
edge(16, 44).
edge(16, 50).
edge(16, 67).
edge(16, 87).
edge(16, 93).
edge(17, 58).
edge(18, 38).
edge(20, 98).
edge(20, 69).
edge(21, 2).
edge(21, 57).
edge(22, 12).
edge(23, 12).
edge(23, 22).
edge(23, 35).
edge(23, 36).
edge(23, 40).
edge(23, 46).
edge(23, 56).
edge(23, 61).
edge(23, 63).
edge(23, 72).
edge(23, 74).
edge(23, 90).
edge(23, 8).
edge(24, 65).
edge(25, 31).
edge(26, 12).
edge(26, 57).
edge(26, 65).
edge(27, 58).
edge(27, 12).
edge(28, 67).
edge(29, 31).
edge(30, 19).
edge(32, 25).
edge(32, 27).
edge(32, 60).
edge(32, 64).
edge(32, 70).
edge(32, 89).
edge(33, 24).
edge(35, 78).
edge(35, 95).
edge(36, 34).
edge(36, 42).
edge(37, 28).
edge(38, 95).
edge(38, 31).
edge(38, 65).
edge(39, 75).
edge(40, 66).
edge(40, 77).
edge(41, 65).
edge(42, 77).
edge(42, 81).
edge(43, 3).
edge(43, 42).
edge(43, 58).
edge(43, 69).
edge(43, 84).
edge(43, 94).
edge(44, 55).
edge(44, 48).
edge(45, 39).
edge(45, 26).
edge(46, 9).
edge(47, 8).
edge(47, 45).
edge(47, 49).
edge(47, 82).
edge(48, 68).
edge(49, 31).
edge(50, 21).
edge(51, 65).
edge(51, 89).
edge(52, 67).
edge(53, 82).
edge(55, 85).
edge(56, 34).
edge(56, 1).
edge(57, 14).
edge(57, 78).
edge(58, 88).
edge(58, 67).
edge(59, 66).
edge(59, 75).
edge(59, 81).
edge(60, 73).
edge(61, 38).
edge(62, 15).
edge(62, 36).
edge(63, 51).
edge(63, 14).
edge(64, 37).
edge(64, 53).
edge(65, 54).
edge(67, 60).
edge(69, 53).
edge(70, 89).
edge(71, 74).
edge(72, 78).
edge(72, 55).
edge(73, 42).
edge(74, 73).
edge(74, 66).
edge(74, 12).
edge(75, 89).
edge(76, 5).
edge(76, 9).
edge(76, 24).
edge(76, 51).
edge(76, 53).
edge(76, 55).
edge(76, 2).
edge(79, 86).
edge(79, 2).
edge(80, 15).
edge(80, 21).
edge(80, 52).
edge(80, 83).
edge(80, 85).
edge(80, 98).
edge(81, 69).
edge(82, 41).
edge(82, 54).
edge(83, 52).
edge(83, 49).
edge(84, 68).
edge(84, 6).
edge(84, 74).
edge(85, 19).
edge(85, 54).
edge(85, 31).
edge(85, 48).
edge(87, 39).
edge(88, 68).
edge(89, 29).
edge(89, 19).
edge(90, 8).
edge(91, 6).
edge(91, 29).
edge(92, 44).
edge(93, 82).
edge(93, 6).
edge(94, 15).
edge(95, 26).
edge(96, 26).
edge(97, 2).
edge(97, 26).
edge(97, 28).
edge(97, 29).
edge(97, 71).
edge(97, 73).
edge(98, 40).
edge(99, 8).
edge(99, 38).
edge(100, 48).
edge(100, 65).
edge(100, 91).
edge(100, 99).
edge(100, 50).
edge(100, 77).
input(97).
input(100).
input(4).
input(7).
input(11).
input(76).
input(43).
input(13).
input(47).
input(16).
input(80).
input(18).
input(23).
input(59).
input(32).
output(34).
output(66).
output(68).
output(77).
output(78).
output(14).
output(19).
output(86).
output(54).
output(31).

test_pair(I, O) :- input(I), output(O).
{ selected(I, O) : test_pair(I, O) }.

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
% #minimize { 1, I, O : selected(I, O) }.
:~ selected(I, O). [1@1, I, O]
