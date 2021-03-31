bash passenger_request.sh pid=$!
PID_LIST+=" $pid";
python3 taxi_metric.py >> taxi_metric.txt pid=$!
PID_LIST+=" $pid";
trap "kill $PID_LIST" SIGINT
wait $PID_LIST
