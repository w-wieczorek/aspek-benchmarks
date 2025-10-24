% Definicja przedmiotów: item(nazwa, waga, wartość)
item(1, 5, 100). item(2, 8, 150). item(3, 3, 80). item(4, 6, 120). item(5, 4, 90).
item(6, 7, 140). item(7, 2, 60). item(8, 9, 180). item(9, 5, 110). item(10, 6, 130).
item(11, 3, 70). item(12, 8, 160). item(13, 4, 95). item(14, 7, 145). item(15, 2, 55).
item(16, 6, 125). item(17, 5, 105). item(18, 9, 175). item(19, 3, 85). item(20, 7, 150).
item(21, 4, 100). item(22, 8, 170). item(23, 2, 65). item(24, 6, 135). item(25, 5, 115).
item(26, 7, 155). item(27, 3, 75). item(28, 9, 185). item(29, 4, 92). item(30, 6, 128).
item(31, 8, 165). item(32, 2, 58). item(33, 5, 108). item(34, 7, 148). item(35, 3, 82).
item(36, 6, 122). item(37, 4, 98). item(38, 9, 178). item(39, 5, 112). item(40, 8, 162).
item(41, 3, 72). item(42, 7, 142). item(43, 2, 62). item(44, 6, 132). item(45, 5, 118).
item(46, 9, 182). item(47, 4, 96). item(48, 8, 168). item(49, 3, 78). item(50, 7, 152).

% Maksymalna pojemność plecaka
capacity(100).

% Generator wyboru: każdy przedmiot może być wybrany lub nie
{ select(I) : item(I, _, _) }.

% Ograniczenie wagi: suma wag wybranych przedmiotów nie może przekroczyć pojemności
:- #sum{ W,I : select(I), item(I, W, _) } > C, capacity(C).

% Optymalizacja: maksymalizuj wartość
:~ not select(I), item(I, _, V). [V@1, I]
