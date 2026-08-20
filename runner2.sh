#!/bin/bash

if command -v python3 >/dev/null 2>&1; then
    PROGRAM="python3"
elif command -v python >/dev/null 2>&1; then
    PROGRAM="python" 
else
    echo "Python not found. Please install Python 3."
    exit 1
fi

folders=("connected-maximum-density-still-life" "degree-bounded-connected-subgraph" "dominating-set" "fault-detection-in-directed-graphs" "feedback-arc-set" "knight-tour-with-holes" "longest-circuit" "longest-path" "maximal-clique" "maximum-leaf-spanning-tree" "minimum-cover" "set-packing" "solitaire" "stacker-crane" "visit-all")
problems=("p1.lp" "p2.lp" "p3.lp" "p4.lp" "p5.lp" "p6.lp" "p7.lp" "p8.lp" "p9.lp" "p10.lp")
CUR_DIR="$(pwd)"

kill_solver_processes() {
    pkill -f clingo 2>/dev/null
    pkill -f dlv 2>/dev/null
    pkill -f cplex 2>/dev/null
    pkill -f gurobi_cl 2>/dev/null
    pkill -f wmaxcdcl_static 2>/dev/null
}

for folder in "${folders[@]}"; do
    for problem in "${problems[@]}"; do
        problem_filepath="$folder/$problem"
        encoding_filepath="$folder/encoding.lp"
        if [ -f "$problem_filepath" ] && [ -f "$encoding_filepath" ]; then
            #"$PROGRAM" monitor.py -t 600 "dlv --mode=idlv --no-facts $problem_filepath $encoding_filepath | lp2normal2 -ok -E | aspirena"
            #kill_solver_processes
            #sleep 5
            "$PROGRAM" monitor.py -t 600 "acyc2solver_mip_fvs_smodels_gurobi.sh $problem_filepath $encoding_filepath"
            kill_solver_processes
            sleep 5
            "$PROGRAM" monitor.py -t 600 "acyc2solver_mip_ve_smodels_gurobi.sh $problem_filepath $encoding_filepath"
            kill_solver_processes
            sleep 5
        else
            echo "File $problem_filepath or $encoding_filepath not found, skipping."
        fi
    done
done
