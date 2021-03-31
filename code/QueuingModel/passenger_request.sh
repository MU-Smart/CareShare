while IFS=, read -r col1 col2 col3 col4 col5 col6
do
	python3 passenger_generalised.py $col4 $col5 $col2 $col3 $col1 >> logs_passenger/$col1.log & pid=$!;
	PID_LIST+=" $pid";
	sleep ${col6::-1};

	
done < "Pass_Requests/Sun_NonPeak_passenger.csv" 


trap "kill $PID_LIST" SIGINT

echo "Passenger processes have started";

wait $PID_LIST

echo
echo "All passenger requests have completed";
