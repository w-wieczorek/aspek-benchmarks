#!/bin/bash

if command -v python3 >/dev/null 2>&1; then
    PROGRAM="python3"
elif command -v python >/dev/null 2>&1; then
    PROGRAM="python" 
else
    echo "Python not found. Please install Python 3."
    exit 1
fi

# Problem instances are selected based on random.org's results with the following parameters:
# https://www.random.org/integers/?num=15&min=1&max=10&col=1&base=10&format=html&rnd=new
problem_filepaths=("connected-maximum-density-still-life/p2.lp" "degree-bounded-connected-subgraph/p8.lp" "dominating-set/p1.lp" "fault-detection-in-directed-graphs/p9.lp" "feedback-arc-set/p10.lp" "knight-tour-with-holes/p3.lp" "longest-circuit/p1.lp" "longest-path/p4.lp" "maximal-clique/p2.lp" "maximum-leaf-spanning-tree/p8.lp" "minimum-cover/p3.lp" "set-packing/p6.lp" "solitaire/p5.lp" "stacker-crane/p10.lp" "visit-all/p3.lp")

CUR_DIR="$(pwd)"


for problem_filepath in "${problem_filepaths[@]}"; do
    encoding_filepath="${problem_filepath%.lp}/encoding.lp"
    if [ -f "$problem_filepath" ] && [ -f "$encoding_filepath" ]; then
        "$PROGRAM" monitor.py -t 600 "mingo.sh $problem_filepath $encoding_filepath"
        "$PROGRAM" monitor.py -t 600 "acyc2solver_mip_fvs.sh $problem_filepath $encoding_filepath"
        "$PROGRAM" monitor.py -t 600 "acyc2solver_mip_ve.sh $problem_filepath $encoding_filepath"
    else
        echo "File $problem_filepath or $encoding_filepath not found, skipping."
    fi
done
