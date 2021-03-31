i=4999
while IFS=, read -r col1 col2 col3
do
	i=$((i+1));
	python3 taxi.py $i $col2 $col3 >> logs_taxis/taxi_$i.log & pid=$!
	PID_LIST+=" $pid";
done < 1dayP_500taxis_Kmeans.csv

trap "kill $PID_LIST" SIGINT

echo "Parallel processes have started";

wait $PID_LIST

echo
echo "All processes have completed";
