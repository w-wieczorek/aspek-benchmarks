#!/usr/bin/env python3
"""Sum wall-clock time per solver/switch variant from results.csv."""

import csv
import os
from collections import defaultdict

TIMEOUT = 600.0
CSV_IN = "results.csv"
CSV_OUT = "totals.csv"


def switch_label(smodels, lp2normal2, gurobi) -> str:
    flags = []
    if smodels:
        flags.append("smodels")
    if lp2normal2:
        flags.append("lp2normal2")
    if gurobi:
        flags.append("gurobi")
    else:
        flags.append("cplex")
    return "+".join(flags)


def load_rows(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def summarize(rows):
    stats = defaultdict(lambda: {
        "total": 0.0,
        "solved": 0,
        "unsat": 0,
        "timeout": 0,
        "missing": 0,
        "n": 0,
    })
    for row in rows:
        key = (
            row["Solver"],
            int(row["smodels"]),
            int(row["lp2normal2"]),
            int(row["gurobi"]),
        )
        s = stats[key]
        s["n"] += 1
        status = (row.get("Status") or "").strip()
        time_raw = (row.get("Time") or "").strip()
        if status == "missing" or not time_raw:
            s["missing"] += 1
            s["total"] += TIMEOUT
            continue
        t = float(time_raw)
        if status == "timeout" or t >= TIMEOUT:
            s["timeout"] += 1
            s["total"] += TIMEOUT
        else:
            s["total"] += t
            s["solved"] += 1
            if status == "unsat":
                s["unsat"] += 1
    return stats


def ranked(stats):
    return sorted(stats.items(), key=lambda item: (item[1]["total"], item[0]))


def print_summary(stats):
    print(f"{'#':<3} {'Solver':<24} {'Switches':<28} {'Total(s)':>10} {'T/O':>4} {'Miss':>4} {'Solved':>8}")
    print("-" * 86)
    for i, (key, s) in enumerate(ranked(stats), 1):
        solver, smodels, lp2normal2, gurobi = key
        print(
            f"{i:<3} {solver:<24} {switch_label(smodels, lp2normal2, gurobi):<28} "
            f"{s['total']:10.2f} {s['timeout']:4} {s['missing']:4} "
            f"{s['solved']}/{s['n']}"
        )


def write_csv(stats, path: str):
    fieldnames = [
        "Rank", "Solver", "smodels", "lp2normal2", "gurobi", "Switches",
        "TotalTime", "Timeouts", "Missing", "Solved", "Unsat", "Runs",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, (key, s) in enumerate(ranked(stats), 1):
            solver, smodels, lp2normal2, gurobi = key
            writer.writerow({
                "Rank": i,
                "Solver": solver,
                "smodels": smodels,
                "lp2normal2": lp2normal2,
                "gurobi": gurobi,
                "Switches": switch_label(smodels, lp2normal2, gurobi),
                "TotalTime": f"{s['total']:.2f}",
                "Timeouts": s["timeout"],
                "Missing": s["missing"],
                "Solved": s["solved"],
                "Unsat": s["unsat"],
                "Runs": s["n"],
            })


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    rows = load_rows(CSV_IN)
    stats = summarize(rows)
    print_summary(stats)
    write_csv(stats, CSV_OUT)
    print(f"\nWrote {CSV_OUT} ({len(stats)} variants).")
