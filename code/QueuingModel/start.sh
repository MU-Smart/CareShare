#!/bin/bash

bash start_all_taxis.sh >> bash_taxis_op.txt & pid=$!
PID_LIST+=" $pid";
sleep 200;
python3 seeder.py >> bash_seeder_op.txt & pid=$!
PID_LIST+=" $pid";
sleep 120;
bash start_passenger_process.sh >> bash_passenger_request_op.txt & pid=$!
PID_LIST+=" $pid";

trap "kill -2 $PID_LIST" SIGINT
wait $PID_LIST

