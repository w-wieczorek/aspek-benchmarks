import random

fileName = "p1"
s = 60
m = 80
universum = list(range(s))
collection = []
for i in range(m):
    collection.append(random.sample(universum, random.randint(5, 12)))

with open(fileName+".lp", "w") as f:
    print(f"s(0..{s-1}).", file=f)
    for i in range(m):
        for j in collection[i]:
            print(f"c({i}, {j}).", file=f)
