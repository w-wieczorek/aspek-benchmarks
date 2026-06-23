import csv
from collections import defaultdict
from math import log

CSV_FILE = "results.csv"
SOLVERS = ["dlv", "clingo bnb", "aspirena", "mingo", "maxmodels", "ezsmt", "acyc2solver_mip_fvs", "acyc2solver_mip_ve", "clingo usc"]
LABELS = ["dlv", "clingo\\,\\textsubscript{bnb}", "aspirena", "mingo", "maxmodels", "ezsmt", "acyc2solver\\,$_{\\text{mip}}^{\\text{fvs}}$", "acyc2solver\\,$_{\\text{mip}}^{\\text{ve}}$", "clingo\\,\\textsubscript{usc}"]
TIMEOUT = 600.0
PROBLEM_ORDER = []
PROBLEM_INSTANCE_COUNT = defaultdict(int)

def score_original(num_solved, times):
    n = len(times)
    s = 10
    alpha = 50
    timeout = TIMEOUT
    gamma = 1 - log(1 + s) / log(timeout + s)
    s_p = alpha * num_solved / n
    s_t = (100 - alpha) / (n * gamma) * sum([
        1 - log(min(timeout, max(1, t)) + s) / log(timeout + s)
        for t in times
    ])
    return s_p + s_t

def score_optimal(num_optimal, num_instances):
    """ASP Competition S2 score for optimization domains.

    Assumption: every non-timeout run proves optimality or unsatisfiability.
    """
    if num_instances == 0:
        return 0.0
    return 100.0 * num_optimal / num_instances

# Parse CSV and aggregate stats per problem and solver
problem_solver_results = defaultdict(lambda: defaultdict(list))

with open(CSV_FILE, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        problem = row["Problem"]
        if problem not in PROBLEM_ORDER:
            PROBLEM_ORDER.append(problem)
        PROBLEM_INSTANCE_COUNT[problem] += 1
        for solver in SOLVERS:
            t = float(row[solver])
            problem_solver_results[problem][solver].append(t)

# Calculate summary (per problem and per solver)
summary = defaultdict(lambda: {"solved": 0, "total_time": 0.0, "score": 0, "times": []})

table_header = (
    "\\begin{tabular}{l" + "|crrr"*len(SOLVERS) + "}\n"
    "Problem"
)
for solver in SOLVERS:
    table_header += f" & \\multicolumn{{3}}{{c}}{{{LABELS[SOLVERS.index(solver)]}}}"
table_header += "\\\\\n"

# Subheader: for each solver, the three columns
table_header += " "
for _ in SOLVERS:
    table_header += " & Suc. & Total time & $S_1$ & $S_2$"
table_header += "\\\\\n\\hline\n"

rows = []

for problem in PROBLEM_ORDER:
    row = [problem.replace("-", "\\-")]
    for solver in SOLVERS:
        times = problem_solver_results[problem][solver]
        num_solved = sum([1 for t in times if t < TIMEOUT])
        total_time = sum([min(t, TIMEOUT) for t in times])
        score_1 = score_original(num_solved, times)
        score_2 = score_optimal(num_solved, len(times))
        row.extend([
            f"{num_solved}/{len(times)}",
            f"{total_time:.2f}",
            f"{score_1}",
            f"{score_2}"
        ])
        # Summing up for totals:
        summary[solver]["solved"] += num_solved
        summary[solver]["total_time"] += total_time
        summary[solver]["times"].extend(times)
    rows.append(" & ".join(row) + " \\\\")

# Now final summary row:
sumrow = ["\\textbf{Total}"]
for solver in SOLVERS:
    total_instances = sum([PROBLEM_INSTANCE_COUNT[p] for p in PROBLEM_ORDER])
    num_solved = summary[solver]["solved"]
    total_time = summary[solver]["total_time"]
    score = score_original(num_solved, summary[solver]["times"])
    sumrow.extend([
        f"{num_solved}/{total_instances}",
        f"{total_time:.2f}",
        f"{score}"
    ])
rows.append(" & ".join(sumrow) + " \\\\")

for solver in SOLVERS:
    print("\\begin{table}[htbp]")
    print("\\centering")
    print(f"\\caption{{Performance of \\textsc{{{LABELS[SOLVERS.index(solver)]}}} across all problems.}}")
    print("\\label{tab:performance-" + solver.replace(" ", "_") + "}")
    print("\\begin{tabular}{lcrrr}")
    print("\\toprule")
    print(
        "Problem & Suc. & Total time & $S_1$ & $S_2$ \\\\"
    )
    print("\\midrule")
    rows = []
    total_score_1 = 0.0
    total_score_2 = 0.0
    for problem in PROBLEM_ORDER:
        times = problem_solver_results[problem][solver]
        num_solved = sum([1 for t in times if t < TIMEOUT])
        total_time = sum([min(t, TIMEOUT) for t in times])
        score_1 = score_original(num_solved, times)
        score_2 = score_optimal(num_solved, len(times))
        total_score_1 += score_1
        total_score_2 += score_2
        rows.append(
            f"{problem} & {num_solved}/{len(times)} & {total_time:.2f}\\,s & {int(score_1)} & {int(score_2)} \\\\"
        )
    # Add summary row
    total_instances = sum([PROBLEM_INSTANCE_COUNT[p] for p in PROBLEM_ORDER])
    num_solved = summary[solver]["solved"]
    total_time = summary[solver]["total_time"]
    rows.append("\\midrule")
    rows.append(
        f"\\textbf{{Total}} & {num_solved}/{total_instances} & {total_time:.2f}\\,s & {int(total_score_1)} & {int(total_score_2)} \\\\"
    )
    for r in rows:
        print(r)
    print("\\botrule")
    print("\\end{tabular}")
    print("\\end{table}\n")


# Compute and print the final standings based on total score (higher is better)
standings = []
for solver in SOLVERS:
    # Recompute total score as above to match what was printed in tables
    total_score = 0
    total_time = 0.0
    for problem in PROBLEM_ORDER:
        times = problem_solver_results[problem][solver]
        num_solved = sum([1 for t in times if t < TIMEOUT])
        score = score_original(num_solved, times)
        total_score += score
        total_time += sum([min(t, TIMEOUT) for t in times])
    standings.append((solver, int(total_score), total_time))
# Sort by descending score, then ascending runtime as tie-breaker
standings.sort(key=lambda x: (-x[1], x[2]))
print("\\begin{table}[htbp]")
print("\\centering")
print("\\caption{Final standings based on the total $S_1$ score (higher is better).}")
print("\\label{tab:final-standings-s1}")
print("\\begin{tabular}{clrr}")
print("\\toprule")
print("Rank & Solver & Total $S_1$ & Total time \\\\")
print("\\midrule")
for idx, (solver, score, total_time) in enumerate(standings, start=1):
    print(f"{idx} & \\textsc{{{LABELS[SOLVERS.index(solver)]}}} & {score} & {total_time:.2f}\\,s \\\\")
print("\\botrule")
print("\\end{tabular}")
print("\\end{table}\n")


# Compute and print S2 standings from the ASP Competition optimization scoring scheme.
s2_standings = []
for solver in SOLVERS:
    total_s2_score = 0.0
    total_time = 0.0
    for problem in PROBLEM_ORDER:
        times = problem_solver_results[problem][solver]
        num_optimal = sum([1 for t in times if t < TIMEOUT])
        total_s2_score += score_optimal(num_optimal, len(times))
        total_time += sum([min(t, TIMEOUT) for t in times])
    s2_standings.append((solver, int(total_s2_score), total_time))
s2_standings.sort(key=lambda x: (-x[1], x[2]))

print("\\begin{table}[htbp]")
print("\\centering")
print("\\caption{Final standings based on the total $S_2$ score (higher is better).}")
print("\\label{tab:final-standings-s2}")
print("\\begin{tabular}{clrr}")
print("\\toprule")
print("Rank & Solver & Total $S_2$ & Total time \\\\")
print("\\midrule")
for idx, (solver, score, total_time) in enumerate(s2_standings, start=1):
    print(f"{idx} & \\textsc{{{LABELS[SOLVERS.index(solver)]}}} & {score} & {total_time:.2f}\\,s \\\\")
print("\\botrule")
print("\\end{tabular}")
print("\\end{table}\n")

