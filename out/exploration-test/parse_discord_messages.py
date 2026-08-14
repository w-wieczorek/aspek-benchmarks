import csv
import glob
import json
import os
import re
from collections import defaultdict
from itertools import product
from typing import Dict, List, Optional, Tuple

TIMEOUT_THRESHOLD = 600.0

PROBLEMS = [
    ("connected-maximum-density-still-life", "p2"),
    ("degree-bounded-connected-subgraph", "p8"),
    ("dominating-set", "p1"),
    ("fault-detection-in-directed-graphs", "p9"),
    ("feedback-arc-set", "p10"),
    ("knight-tour-with-holes", "p3"),
    ("longest-circuit", "p1"),
    ("longest-path", "p4"),
    ("maximal-clique", "p2"),
    ("maximum-leaf-spanning-tree", "p8"),
    ("minimum-cover", "p3"),
    ("set-packing", "p6"),
    ("solitaire", "p5"),
    ("stacker-crane", "p10"),
    ("visit-all", "p3"),
]

SOLVERS = ["mingo", "acyc2solver_mip_fvs", "acyc2solver_mip_ve"]
SWITCH_NAMES = ["smodels", "lp2normal2", "gurobi"]


def expected_configs() -> List[Tuple[str, int, int, int]]:
    configs = []
    for solver in SOLVERS:
        for smodels, lp2normal2, gurobi in product((0, 1), repeat=3):
            if solver == "mingo" and gurobi:
                continue
            configs.append((solver, smodels, lp2normal2, gurobi))
    return configs


EXPECTED_CONFIGS = expected_configs()


def parse_script_name(script: str) -> Optional[Tuple[str, int, int, int]]:
    name = script.strip()
    if name.endswith(".sh"):
        name = name[:-3]
    solver = None
    for candidate in sorted(SOLVERS, key=len, reverse=True):
        if name == candidate or name.startswith(candidate + "_"):
            solver = candidate
            rest = name[len(candidate):].lstrip("_")
            break
    if solver is None:
        return None
    parts = set(rest.split("_")) if rest else set()
    parts.discard("")
    unknown = parts - set(SWITCH_NAMES)
    if unknown:
        return None
    return (
        solver,
        int("smodels" in parts),
        int("lp2normal2" in parts),
        int("gurobi" in parts),
    )


def extract_command_info(description: str) -> Optional[Tuple[str, str, str, int, int, int]]:
    cmd_match = re.search(r"Command:\s+([^\s]+)\s+(\S+)", description)
    if not cmd_match:
        return None
    parsed = parse_script_name(cmd_match.group(1))
    if not parsed:
        return None
    solver, smodels, lp2normal2, gurobi = parsed
    path_match = re.search(r"([\w-]+)/(p\d+)\.lp", cmd_match.group(2))
    if not path_match:
        path_match = re.search(r"([\w-]+)/(p\d+)\.lp", description)
    if not path_match:
        return None
    return (solver, path_match.group(1), path_match.group(2), smodels, lp2normal2, gurobi)


def extract_execution_time(description: str) -> Optional[float]:
    match = re.search(
        r"Total execution time \(including monitoring overhead\):\s+([\d.]+)\s+seconds",
        description,
    )
    if match:
        return float(match.group(1))
    return None


def extract_objective(description: str) -> Optional[float]:
    cplex = re.search(r'<objective\b[^>]*\bvalue="([^"]+)"', description)
    if cplex:
        try:
            return float(cplex.group(1))
        except ValueError:
            return None
    matches = re.findall(
        r"Objective:\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)",
        description,
    )
    if matches:
        try:
            return float(matches[-1])
        except ValueError:
            return None
    return None


def is_unsat(description: str) -> bool:
    markers = (
        "UNSATISFIABLE",
        "Model is infeasible",
        "No solution exists",
        "CPLEX Error 1217",
    )
    return any(marker in description for marker in markers)


def config_key(solver: str, smodels: int, lp2normal2: int, gurobi: int) -> Tuple[str, int, int, int]:
    return (solver, smodels, lp2normal2, gurobi)


def parse_messages(messages: list) -> Dict[Tuple[str, str], Dict[Tuple[str, int, int, int], dict]]:
    results = defaultdict(dict)
    for message in messages:
        for embed in message.get("embeds") or []:
            description = embed.get("description")
            if not description:
                continue
            cmd_info = extract_command_info(description)
            if not cmd_info:
                continue
            solver, problem_name, dataset, smodels, lp2normal2, gurobi = cmd_info
            exec_time = extract_execution_time(description)
            if exec_time is None:
                continue
            key = config_key(solver, smodels, lp2normal2, gurobi)
            instance = (problem_name, dataset)
            title = embed.get("title") or ""
            timed_out = "Terminated" in title or exec_time >= TIMEOUT_THRESHOLD
            unsat = (not timed_out) and is_unsat(description)
            record = {
                "time": exec_time,
                "objective": None if timed_out or unsat else extract_objective(description),
                "timeout": timed_out,
                "unsat": unsat,
            }
            if key not in results[instance]:
                results[instance][key] = record
    return dict(results)


def format_time(seconds: float, timed_out: bool = False) -> str:
    if timed_out or seconds >= TIMEOUT_THRESHOLD:
        return "T/O"
    return f"{seconds:.2f}s"


def format_objective(value: Optional[float]) -> str:
    if value is None:
        return ""
    if float(value).is_integer():
        return str(int(value))
    return f"{value:g}"


def format_config(solver: str, smodels: int, lp2normal2: int, gurobi: int) -> str:
    flags = []
    if smodels:
        flags.append("smodels")
    if lp2normal2:
        flags.append("lp2normal2")
    if gurobi:
        flags.append("gurobi")
    return f"{solver}[{'+'.join(flags) or 'default'}]"


def missing_runs(results: Dict[Tuple[str, str], Dict[Tuple[str, int, int, int], dict]]) -> List[dict]:
    missing = []
    for problem_name, dataset in PROBLEMS:
        present = results.get((problem_name, dataset), {})
        for config in EXPECTED_CONFIGS:
            if config not in present:
                solver, smodels, lp2normal2, gurobi = config
                missing.append({
                    "Problem": problem_name,
                    "Dataset": dataset,
                    "Solver": solver,
                    "smodels": smodels,
                    "lp2normal2": lp2normal2,
                    "gurobi": gurobi,
                    "Config": format_config(*config),
                })
    return missing


def generate_summary(results, missing) -> str:
    output = []
    output.append("=" * 72)
    output.append("EXPLORATION TEST RESULTS")
    output.append("=" * 72)
    output.append(
        f"Expected: {len(PROBLEMS)} problems x {len(EXPECTED_CONFIGS)} configs "
        f"= {len(PROBLEMS) * len(EXPECTED_CONFIGS)} runs"
    )
    found = sum(len(cfgs) for cfgs in results.values())
    output.append(f"Found:    {found} runs")
    output.append(f"Missing:  {len(missing)} runs")

    output.append("")
    output.append("=" * 72)
    output.append("MISSING RUNS (re-run these)")
    output.append("=" * 72)
    if not missing:
        output.append("None.")
    else:
        by_instance = defaultdict(list)
        for row in missing:
            by_instance[(row["Problem"], row["Dataset"])].append(row["Config"])
        for problem_name, dataset in PROBLEMS:
            configs = by_instance.get((problem_name, dataset))
            if not configs:
                continue
            output.append(f"\n{problem_name}/{dataset}.lp  ({len(configs)} missing)")
            for cfg in configs:
                output.append(f"  - {cfg}")

    output.append("")
    output.append("=" * 72)
    output.append("OBJECTIVE VALUES")
    output.append("=" * 72)
    for problem_name, dataset in PROBLEMS:
        present = results.get((problem_name, dataset), {})
        if not present:
            continue
        output.append(f"\n{problem_name}/{dataset}.lp")
        for config in EXPECTED_CONFIGS:
            record = present.get(config)
            label = format_config(*config)
            if record is None:
                output.append(f"  {label:<55} MISSING")
                continue
            time_s = format_time(record["time"], record["timeout"])
            if record["timeout"]:
                obj = "T/O"
            elif record["unsat"]:
                obj = "UNSAT"
            elif record["objective"] is None:
                obj = "N/A"
            else:
                obj = format_objective(record["objective"])
            output.append(f"  {label:<55} obj={obj:<12} time={time_s}")

    return "\n".join(output)


def export_results_csv(results, csv_file: str):
    fieldnames = [
        "Problem", "Dataset", "Solver", "smodels", "lp2normal2", "gurobi",
        "Time", "Objective", "Status",
    ]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for problem_name, dataset in PROBLEMS:
            present = results.get((problem_name, dataset), {})
            for config in EXPECTED_CONFIGS:
                solver, smodels, lp2normal2, gurobi = config
                record = present.get(config)
                row = {
                    "Problem": problem_name,
                    "Dataset": dataset,
                    "Solver": solver,
                    "smodels": smodels,
                    "lp2normal2": lp2normal2,
                    "gurobi": gurobi,
                    "Time": "",
                    "Objective": "",
                    "Status": "missing",
                }
                if record:
                    row["Time"] = record["time"]
                    if record["timeout"]:
                        row["Status"] = "timeout"
                    elif record["unsat"]:
                        row["Status"] = "unsat"
                    else:
                        row["Status"] = "solved"
                    if record["objective"] is not None:
                        row["Objective"] = format_objective(record["objective"])
                writer.writerow(row)


def export_missing_csv(missing, csv_file: str):
    fieldnames = ["Problem", "Dataset", "Solver", "smodels", "lp2normal2", "gurobi", "Config"]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(missing)


def load_messages() -> list:
    messages = []
    json_files = sorted(glob.glob("obliczenia-page-*.json") + glob.glob("obliczenia_page_*.json"))
    if not json_files:
        raise FileNotFoundError("No obliczenia-page-*.json files found in the current directory.")
    for path in json_files:
        with open(path, "r", encoding="utf-8") as f:
            messages.extend(json.load(f))
    return messages


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    messages = load_messages()
    results = parse_messages(messages)
    if not results:
        print("No results found!")
        raise SystemExit(1)
    missing = missing_runs(results)
    print(generate_summary(results, missing))
    export_results_csv(results, "results.csv")
    export_missing_csv(missing, "missing.csv")
    print(f"\nWrote results.csv ({len(PROBLEMS) * len(EXPECTED_CONFIGS)} rows) and missing.csv ({len(missing)} rows).")
