import csv
from collections import defaultdict
from math import log

CSV_FILE = "results.csv"
SOLVERS = ["dlv", "clingo", "aspirena", "mingo"]
TIMEOUT = 600.0
PROBLEM_ORDER = []
PROBLEM_INSTANCE_COUNT = defaultdict(int)

def score_placeholder(num_solved, times):
    n = 10
    s = 10
    alpha = 50
    timeout = 600
    gamma = 1 - log(1 + s) / log(timeout + s)
    s_p  = alpha * num_solved / n
    s_t = (100 - alpha) / (n * gamma) * sum([1 - log(min(timeout, max(1, t)) + s) / log(timeout + s) for t in times])
    return s_p + s_t

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
    "\\begin{tabular}{l" + "|ccc"*len(SOLVERS) + "}\n"
    "Problem"
)
for solver in SOLVERS:
    table_header += f" & \\multicolumn{{3}}{{c}}{{{solver}}}"
table_header += "\\\\\n"

# Subheader: for each solver, the three columns
table_header += " "
for _ in SOLVERS:
    table_header += " & Suc. & Time & Score"
table_header += "\\\\\n\\hline\n"

rows = []

for problem in PROBLEM_ORDER:
    row = [problem.replace("-", "\\-")]
    for solver in SOLVERS:
        times = problem_solver_results[problem][solver]
        num_solved = sum([1 for t in times if t < TIMEOUT])
        total_time = sum([t for t in times if t < TIMEOUT])
        score = score_placeholder(num_solved, times)
        row.extend([
            f"{num_solved}/{len(times)}",
            f"{total_time:.2f}",
            f"{score}"
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
    score = score_placeholder(num_solved, summary[solver]["times"])
    sumrow.extend([
        f"{num_solved}/{total_instances}",
        f"{total_time:.2f}",
        f"{score}"
    ])
rows.append(" & ".join(sumrow) + " \\\\")

for solver in SOLVERS:
    print("\\begin{table}")
    print("\\centering")
    print(f"\\caption{{Performance of \\textsc{{{solver}}} across all problems.}}")
    print("\\label{tab:performance-" + solver + "}")
    print("\\begin{tabular}{| l | c | r | r |}")
    print("\\hline")
    print(
        "Problem & Suc. & Time & Score \\\\"
    )
    print("\\hline")
    rows = []
    total_score = 0.0
    for problem in PROBLEM_ORDER:
        times = problem_solver_results[problem][solver]
        num_solved = sum([1 for t in times if t < TIMEOUT])
        total_time = sum([t if t < TIMEOUT else 600.0 for t in times])
        score = score_placeholder(num_solved, times)
        total_score += score
        rows.append(
            f"{problem} & {num_solved}/{len(times)} & {total_time:.2f}\\,s & {int(score)} \\\\"
        )
    # Add summary row
    total_instances = sum([PROBLEM_INSTANCE_COUNT[p] for p in PROBLEM_ORDER])
    num_solved = summary[solver]["solved"]
    total_time = summary[solver]["total_time"]
    rows.append("\\hline")
    rows.append(
        f"\\textbf{{Total}} & {num_solved}/{total_instances} & {total_time:.2f}\\,s & {int(total_score)} \\\\"
    )
    for r in rows:
        print(r)
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table}\n")


# Compute and print the final standings based on total score (higher is better)
standings = []
for solver in SOLVERS:
    # Recompute total score as above to match what was printed in tables
    total_score = 0
    for problem in PROBLEM_ORDER:
        times = problem_solver_results[problem][solver]
        num_solved = sum([1 for t in times if t < TIMEOUT])
        score = score_placeholder(num_solved, times)
        total_score += score
    standings.append((solver, int(total_score)))
# Sort by descending score
standings.sort(key=lambda x: x[1], reverse=True)
print("\\begin{table}")
print("\\centering")
print("\\caption{Final standings based on total score (higher is better).}")
print("\\label{tab:final-standings}")
print("\\begin{tabular}{|c|l|r|}")
print("\\hline")
print("Rank & Solver & Score \\\\")
print("\\hline")
for idx, (solver, score) in enumerate(standings, start=1):
    print(f"{idx} & \\textsc{{{solver}}} & {score} \\\\")
print("\\hline")
print("\\end{tabular}")
print("\\end{table}\n")

