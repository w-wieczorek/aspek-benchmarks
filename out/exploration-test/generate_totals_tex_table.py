#!/usr/bin/env python3
"""Generate a booktabs standings table from totals.csv."""

import csv
import os

CSV_FILE = "totals.csv"

SOLVER_LABELS = {
    "acyc2solver_mip_fvs": r"acyc2solver\,$_{\text{mip}}^{\text{fvs}}$",
    "acyc2solver_mip_ve": r"acyc2solver\,$_{\text{mip}}^{\text{ve}}$",
    "mingo": "mingo",
}


def solver_label(name: str) -> str:
    return SOLVER_LABELS.get(name, name.replace("_", r"\_"))


def mip_solver(gurobi: str) -> str:
    return "\\textsc{gurobi}" if int(gurobi) else "\\textsc{cplex}"


def mark(flag: str) -> str:
    return "$+$" if int(flag) else ""


def main() -> None:
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(r"\begin{table}[htbp]")
    print(r"\centering")
    print(
        r"\caption{Standings of the toolchain configurations of the solver \\textsc{acyc2solver} ranked by total time "
        r"(lower is better).}"
    )
    print(r"\label{tab:exploration-standings}")
    print(r"\begin{tabular}{clccccr}")
    print(r"\toprule")
    print(
        r"Rank & Solver & \\texttt{smodels} & \\texttt{lp2normal2} & MIP solver & Suc. & Total time \\"
    )
    print(r"\midrule")
    for row in rows:
        label = solver_label(row["Solver"])
        print(
            f"{row['Rank']} & \\textsc{{{label}}} & "
            f"{mark(row['smodels'])} & {mark(row['lp2normal2'])} & "
            f"{mip_solver(row['gurobi'])} & "
            f"{row['Solved']}/{row['Runs']} & {row['TotalTime']}\\,s \\\\"
        )
    print(r"\botrule")
    print(r"\end{tabular}")
    print(r"\end{table}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
