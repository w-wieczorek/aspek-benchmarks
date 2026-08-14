#!/bin/bash

if command -v python3 >/dev/null 2>&1; then
    PROGRAM="python3"
elif command -v python >/dev/null 2>&1; then
    PROGRAM="python"
else
    echo "Python not found. Please install Python 3."
    exit 1
fi

kill_solver_processes() {
    pkill -f clingo 2>/dev/null
    pkill -f dlv 2>/dev/null
    pkill -f cplex 2>/dev/null
    pkill -f gurobi_cl 2>/dev/null
    pkill -f wmaxcdcl_static 2>/dev/null
}

# Missing runs from out/exploration-test/missing.csv (19 entries).
# Format: "<solver-script> <problem.lp>"
runs=(
    "acyc2solver_mip_ve_smodels_gurobi.sh connected-maximum-density-still-life/p2.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh degree-bounded-connected-subgraph/p8.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh dominating-set/p1.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh fault-detection-in-directed-graphs/p9.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh feedback-arc-set/p10.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh knight-tour-with-holes/p3.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh longest-circuit/p1.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh longest-path/p4.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh maximal-clique/p2.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh maximum-leaf-spanning-tree/p8.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh minimum-cover/p3.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh set-packing/p6.lp"
    "acyc2solver_mip_ve_gurobi.sh solitaire/p5.lp"
    "acyc2solver_mip_ve_lp2normal2.sh solitaire/p5.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh solitaire/p5.lp"
    "acyc2solver_mip_ve_smodels_lp2normal2.sh solitaire/p5.lp"
    "acyc2solver_mip_ve_smodels_lp2normal2_gurobi.sh solitaire/p5.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh stacker-crane/p10.lp"
    "acyc2solver_mip_ve_smodels_gurobi.sh visit-all/p3.lp"
)

total="${#runs[@]}"
index=0
for run in "${runs[@]}"; do
    index=$((index + 1))
    script="${run%% *}"
    problem_filepath="${run#* }"
    encoding_filepath="$(dirname "$problem_filepath")/encoding.lp"
    echo "[$index/$total] $script $problem_filepath"
    if [ -f "$problem_filepath" ] && [ -f "$encoding_filepath" ]; then
        "$PROGRAM" monitor.py -t 600 "$script $problem_filepath $encoding_filepath"
        kill_solver_processes
        sleep 5
    else
        echo "File $problem_filepath or $encoding_filepath not found, skipping."
    fi
done
