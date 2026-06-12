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


for folder in "${folders[@]}"; do
    for problem in "${problems[@]}"; do
        problem_filepath="$folder/$problem"
        encoding_filepath="$folder/encoding.lp"
        if [ -f "$problem_filepath" ] && [ -f "$encoding_filepath" ]; then
            #"$PROGRAM" monitor.py -t 600 "dlv --mode=idlv --no-facts $problem_filepath $encoding_filepath | lp2normal2 -ok -E | aspirena"
            #sync && echo 3 | tee /proc/sys/vm/drop_caches
            #"$PROGRAM" monitor.py -t 600 "mingo.sh $problem_filepath $encoding_filepath"
            #sync && echo 3 | tee /proc/sys/vm/drop_caches
            #"$PROGRAM" monitor.py -t 600 "clingo $problem_filepath $encoding_filepath"
            #sync && echo 3 | tee /proc/sys/vm/drop_caches
            #"$PROGRAM" monitor.py -t 600 "dlv $problem_filepath $encoding_filepath"
            #sync && echo 3 | tee /proc/sys/vm/drop_caches
            "$PROGRAM" monitor.py -t 600 "maxmodels.sh $problem_filepath $encoding_filepath"
            "$PROGRAM" monitor.py -t 600 "clingo --opt-strategy=usc $problem_filepath $encoding_filepath"
            "$PROGRAM" monitor.py -t 600 "ezsmt -s cvc5 $problem_filepath $encoding_filepath"
            "$PROGRAM" monitor.py -t 600 "acyc2solver_mip_fvs.sh $problem_filepath $encoding_filepath"
            "$PROGRAM" monitor.py -t 600 "acyc2solver_mip_ve.sh $problem_filepath $encoding_filepath"
        else
            echo "File $problem_filepath or $encoding_filepath not found, skipping."
        fi
    done
done
