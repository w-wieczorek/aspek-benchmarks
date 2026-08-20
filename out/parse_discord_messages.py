import json
import re
import sys
import csv
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

def extract_command_info(description: str) -> Optional[Tuple[str, str, str]]:
    match = re.search(r'Command:\s+([^\s]+)', description)
    if not match:
        return None
    command = match.group(1)
    if '|' in description:
        cmd_match = re.search(r'Command:\s+([^\n]+)', description)
        if cmd_match:
            full_cmd = cmd_match.group(1)
            if 'aspirena' in full_cmd:
                solver = 'aspirena'
            else:
                solver = command.split('|')[0].strip()
                solver = re.sub(r'^dlv\s+--mode=idlv\s+--no-facts', 'dlv', solver).strip()
    else:
        solver = command
    if solver.endswith('.sh'):
        solver = solver[:-3]
    if solver == 'mingo.sh':
        solver = 'mingo'
    if solver == 'maxmodels.sh':
        solver = 'maxmodels'
    if solver == 'ezsmt':
        solver = 'ezsmt'
    if solver == 'acyc2solver_mip_fvs.sh':
        solver = 'acyc2solver_mip_fvs'
    if solver == 'acyc2solver_mip_ve.sh':
        solver = 'acyc2solver_mip_ve'
    if solver == 'acyc2solver_mip_ve_smodels_gurobi.sh':
        solver = 'acyc2solver_mip_ve_smodels_gurobi'
    if solver == 'acyc2solver_mip_fvs_smodels_gurobi.sh':
        solver = 'acyc2solver_mip_fvs_smodels_gurobi'
    if solver == 'clingo' and '--opt-strategy=usc' in description:
        solver = 'clingo usc'
    elif solver == 'clingo':
        solver = 'clingo bnb'
    path_match = re.search(r'(\w+(?:-\w+)*)/(p\d+)\.lp', description)
    if path_match:
        problem_name = path_match.group(1)
        dataset = path_match.group(2)
        return (solver, problem_name, dataset)
    return None

def extract_execution_time(description: str) -> Optional[float]:
    match = re.search(r'Total execution time \(including monitoring overhead\):\s+([\d.]+)\s+seconds', description)
    if match:
        return float(match.group(1))
    return None

def parse_messages(messages: list) -> Dict[str, Dict[str, Dict[str, float]]]:
    results = defaultdict(lambda: defaultdict(dict))
    for message in messages:
        if 'embeds' not in message or not message['embeds']:
            continue
        for embed in message['embeds']:
            if 'description' not in embed:
                continue
            description = embed['description']
            cmd_info = extract_command_info(description)
            if not cmd_info:
                continue
            solver, problem_name, dataset = cmd_info
            exec_time = extract_execution_time(description)
            if exec_time is None:
                continue
            if solver not in results[problem_name][dataset]:
                results[problem_name][dataset][solver] = exec_time
    #results[problem_name][dataset][solver] = exec_time
    return dict(results)

def format_time(seconds: float) -> str:
    timeout_threshold = 600.0
    is_timeout = seconds >= timeout_threshold
    if is_timeout:
        result = "T/O"
    else:
        result = f"{seconds:.2f}s"
    return result

def generate_summary(results: Dict[str, Dict[str, Dict[str, float]]]) -> str:
    output = []
    output.append("=" * 47)
    output.append("EXECUTION TIME COMPARISON SUMMARY")
    output.append("=" * 47)
    
    solvers = ['dlv', 'clingo bnb', 'aspirena', 'mingo', 'maxmodels', 'ezsmt', 'acyc2solver_mip_fvs', 'acyc2solver_mip_ve', 'clingo usc', 'acyc2solver_mip_ve_smodels_gurobi', 'acyc2solver_mip_fvs_smodels_gurobi']
    
    for problem_name in sorted(results.keys()):
        output.append(f"\nProblem: {problem_name}")
        output.append("-" * 47)
        
        datasets = sorted(results[problem_name].keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 0)
        
        # Header
        header = f"{'Dataset':<7}"
        for solver in solvers:
            header += f"{solver:>10}"
        output.append(header)
        output.append("-" * 47)
        
        # Data rows
        for dataset in datasets:
            row = f"{dataset:<7}"
            for solver in solvers:
                if solver in results[problem_name][dataset]:
                    time = results[problem_name][dataset][solver]
                    row += f"{format_time(time):>10}"
                else:
                    row += f"{'N/A':>10}"
            output.append(row)
        
        # Summary statistics per problem
        output.append("")
        output.append("Best times per dataset:")
        for dataset in datasets:
            times = {s: t for s, t in results[problem_name][dataset].items() if s in solvers}
            if times:
                best_solver = min(times, key=times.get)
                best_time = times[best_solver]
                output.append(f"  {dataset}: {best_solver} ({format_time(best_time)})")

    # Overall summary
    output.append("")
    output.append("=" * 47)
    output.append("OVERALL STATISTICS")
    output.append("=" * 47)

    # Ranking of solvers per problem by total time (T/O as 600s), with success rate in brackets.
    output.append("")
    output.append("Solver rankings per problem (total time, success rate):")
    for problem_name in sorted(results.keys()):
        solver_totals = {}
        solver_success = {}
        datasets = sorted(results[problem_name].keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 0)
        num_instances = len(datasets)
        for solver in solvers:
            total_time = 0.0
            solved_count = 0
            for dataset in datasets:
                if solver in results[problem_name][dataset]:
                    t = results[problem_name][dataset][solver]
                    if t >= 600.0:  # timeout counted as 600 s
                        total_time += 600.0
                    else:
                        total_time += t
                        solved_count += 1
                else:
                    total_time += 600.0
            solver_totals[solver] = total_time
            solver_success[solver] = solved_count
        ranking = sorted(solver_totals.items(), key=lambda x: x[1])
        output.append(f"Problem: {problem_name}")
        for idx, (solver, total) in enumerate(ranking, 1):
            success_rate = solver_success[solver]
            output.append(f"  {idx}. {solver:8} - Total: {total:.2f}s ({success_rate}/{num_instances})")
        output.append("")
    
    solver_stats = defaultdict(list)
    for problem_name in results:
        for dataset in results[problem_name]:
            for solver, time in results[problem_name][dataset].items():
                if solver in solvers:
                    solver_stats[solver].append(time)
    output.append("")
    output.append("Average execution times by solver:")
    for solver in solvers:
        if solver in solver_stats:
            avg_time = sum(solver_stats[solver]) / len(solver_stats[solver])
            min_time = min(solver_stats[solver])
            max_time = max(solver_stats[solver])
            output.append(f"{solver:10} - Avg: {format_time(avg_time):>8}")
    return "\n".join(output)

def export_to_csv(results: Dict[str, Dict[str, Dict[str, float]]], csv_file: str):
    solvers = ['dlv', 'clingo bnb', 'aspirena', 'mingo', 'maxmodels', 'ezsmt', 'acyc2solver_mip_fvs', 'acyc2solver_mip_ve', 'clingo usc', 'acyc2solver_mip_ve_smodels_gurobi', 'acyc2solver_mip_fvs_smodels_gurobi']
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Problem', 'Dataset'] + solvers)
        for problem_name in sorted(results.keys()):
            datasets = sorted(results[problem_name].keys(), 
                            key=lambda x: int(x[1:]) if x[1:].isdigit() else 0)
            for dataset in datasets:
                row = [problem_name, dataset]
                for solver in solvers:
                    if solver in results[problem_name][dataset]:
                        row.append(results[problem_name][dataset][solver])
                    else:
                        row.append('')
                writer.writerow(row)

messages = []
with open('obliczenia_page_1.json', 'r', encoding='utf-8') as f1, \
     open('obliczenia_page_2.json', 'r', encoding='utf-8') as f2, \
     open('obliczenia_page_3.json', 'r', encoding='utf-8') as f3, \
     open('obliczenia-page-4.json', 'r', encoding='utf-8') as f4:
    messages = json.load(f1)
    messages.extend(json.load(f2))
    messages.extend(json.load(f3))
    messages.extend(json.load(f4))

results = parse_messages(messages)
if not results:
    print("No results found!")
    exit(1)
summary = generate_summary(results)
print(summary)
csv_file = 'results.csv'
export_to_csv(results, csv_file)

