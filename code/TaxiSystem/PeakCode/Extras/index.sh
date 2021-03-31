#!/bin/bash

cmdarray=("python3 taxi.py 5000 41.859406123 -87.6391171652" "python3 taxi.py 5001 41.867406123 -87.617971652" "python3 taxi.py 5002 41.875406123 -87.659971652" "python3 taxi.py 5003 41.877406123 -87.621971652")

echo "Array size: ${#cmdarray[*]}";

for cmdno in ${!cmdarray[*]}; do {
  echo "Process \"$cmdno\" started";
  ${cmdarray[$cmdno]} & pid=$!
  PID_LIST+=" $pid";
} done

trap "kill $PID_LIST" SIGINT

echo "Parallel processes have started";

wait $PID_LIST

echo
echo "All processes have completed";

