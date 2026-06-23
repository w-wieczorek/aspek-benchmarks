# Aspirena Benchmarks

This repository contains benchmark experiments comparing our proposed ASP solver (aspirena) against standard Answer Set Programming solvers (dlv, clingo, and mingo) across a diverse set of combinatorial optimization problems.

## Repository Structure

The repository is organized into multiple problem domains, each containing:

- **`encoding.lp`**: The ASP encoding for the problem
- **`p1.lp` through `p10.lp`**: Problem instances of varying difficulty
- **`README.md`** (in some directories): Baseline timing information and problem descriptions

### Problem Domains

The benchmark suite includes the following problem domains:

- **connected-maximum-density-still-life**: Connected maximum density still life problem (ASP Comp. 2013)
- **degree-bounded-connected-subgraph**: Degree-bounded connected subgraph problem (GT26 in Garey & Johnson)
- **dominating-set**: Dominating set problem (GT2 in Garey & Johnson)
- **fault-detection-in-directed-graphs**: Fault detection in directed graphs (MS18 in Garey & Johnson)
- **feedback-arc-set**: Feedback arc set problem (GT8 in Garey & Johnson)
- **knight-tour-with-holes**: Knight's tour with holes (ASP Comp. 2013)
- **longest-circuit**: Longest circuit problem (ND28 in Garey & Johnson)
- **longest-path**: Longest path problem (ND29 in Garey & Johnson)
- **maximal-clique**: Maximal clique problem (GT19 in Garey & Johnson)
- **maximum-leaf-spanning-tree**: Maximum leaf spanning tree problem (ND2 in Garey & Johnson)
- **minimum-cover**: Minimum cover problem (SP5 in Garey & Johnson)
- **set-packing**: Set packing problem (SP3 in Garey & Johnson)
- **solitaire**: Solitaire problem (ASP Comp. 2013)
- **stacker-crane**: Stacker crane problem (ND26 in Garey & Johnson)
- **visit-all**: Visit-all problem (ASP Comp. 2013)

## Experimental Setup

### Solvers Compared

- **DLV** 2.1.2 (standard ASP solver)
- **Clingo** 5.8.0 (standard ASP solver)
- **Aspirena** our proposed solver (version 1.0)
- **Mingo** (version 2012-09-30) solver
- **acyc2solver** (see [here](https://github.com/asptools/software))
- **ezsmt** (see [here](https://github.com/ylierler/ezsmtv3))
- **maxmodels** (see [here](https://github.com/lazarow/maxmodels-build-II))

### Running Experiments

The `runner.sh` script executes experiments across all problem instances. It runs each solver on each problem instance with a timeout of 600 seconds per run.

The `monitor.py` script monitors process execution, tracks resource usage, and can send notifications (e.g., via Discord webhook) when experiments complete.

### Results

Experimental results are stored in the `out/` directory:

- **`results.csv`**: Raw timing results for all solvers across all problem instances
- **`results.txt`**: Formatted text output of results

## Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

Required packages:

- `psutil>=5.9.0`: Process and system utilities for monitoring
- `requests>=2.31.0`: HTTP library for notifications
- `pypblib`: Python bindings for PBLib

## Usage

To run experiments for a specific problem domain, modify `runner.sh` to specify the folder(s) and execute:

```bash
./runner.sh
```

The script will run all four solvers (dlv, clingo, aspirena, and mingo) on each problem instance in the specified domain(s).

## Authors

Contributors names and contact info:

- [Wojciech Wieczorek](https://kiia.ubb.edu.pl/pracownicy/dr-habwojciechwieczorek),
- [Arkadiusz Nowakowski](https://ab.us.edu.pl/emp?id=46971),
- [Łukasz Strąk](https://ab.us.edu.pl/emp?id=47011).

## License

This project is licensed under the Apache License 2.0 - see the LICENSE.md file for details
