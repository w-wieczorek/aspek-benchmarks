import random
import math
from typing import List, Set
import json

def generate_uniform_random(n: int, m: int, k: int, seed: int) -> List[Set[int]]:
    sets = []
    universe = list(range(n))
    random.seed(seed)
    for _ in range(m):
        selected = set(random.sample(universe, k))
        sets.append(selected)
    return sets

def generate_variable_size_random(n: int, m: int, k_min: int, k_max: int, seed: int) -> List[Set[int]]:
    sets = []
    universe = list(range(n))
    random.seed(seed)
    for _ in range(m):
        k = random.randint(k_min, k_max)
        k = min(k, n)  # Ensure k doesn't exceed universe size
        selected = set(random.sample(universe, k))
        sets.append(selected)
    return sets

def generate_phase_transition(n: int, k: int, seed: int, density_ratio: float = 1.0) -> List[Set[int]]:
    m = int(n * density_ratio / k)
    m = max(m, 1)  # Ensure at least one set
    return generate_uniform_random(n, m, k, seed)

def generate_hard_instance_model_a(n: int, k: int, seed: int) -> List[Set[int]]:
    m = max(1, int(n / k))
    return generate_uniform_random(n, m, k, seed)
    
def generate_hard_instance_model_b(n: int, seed: int) -> List[Set[int]]:
    k = max(2, int(math.sqrt(n)))
    m = max(1, int(math.sqrt(n)))
    return generate_uniform_random(n, m, k, seed)

seeds = [
    (350, 5, 4210067), (400, 5, 1662988), (403, 5, 3086742), (404, 5, 9491513),
    (350, 5, 5655004), (400, 5, 263067), (403, 5, 3454786),
    (200, 5, 2169901), (250, 5, 7187272), (300, 4, 2987890),
]

for i, (n, k, seed) in enumerate(seeds):
    if i < 4:
        sets = generate_phase_transition(n, k, seed)
    elif i < 7:
        sets = generate_hard_instance_model_a(n, k, seed)
    else:
        sets = generate_variable_size_random(n, 80, k-2, k+2, seed)
    with open(f"p{i+1}.lp", "w") as f:
        f.write(f"subset(1..{len(sets)}).\n")
        for j, s in enumerate(sets):
            for e in s:
                f.write(f"c({j+1}, {e}).\n")