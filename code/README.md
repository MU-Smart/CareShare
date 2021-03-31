# Code

The Code folder is organised into the following subfolders:

1. Taxi System: This folder contains the code to run the taxi system. This folder is organised into Non Peak and Peak folders. These folders have the data to run the taxi system respectively during peak and non peak hours. For these folders, any configuration changes such as changing taxi timer values, first hop distance, number of taxis, the port on which the taxis should run can be done. Also the HERE API key to (This API provides the route between two locations. Link : https://developer.here.com/) needs to be updated accordingly in ride_sharing.config. In order to simulate the full scale taxi system we can use any computing cluster (we have used the Miami cluster), we connect to the Miami cluster and then connect to the compute nodes using the below command:

```
qsub -l  nodes = 2:ppn = 4 -l walltime=9:00:00-IV -X
```

Here, nodes, ppn can be configured according to requirements. The value of walltime depends on the number of hours required to run the taxi system. After connecting to the compute node, go to the NonPeak or Peak folder and run the below command:

```
bash start.sh 2>&1 | tee full_op.txt
```

After the taxi system has completed running, the results are present in experiments.csv and experiments_taxis.csv. Any logs will be logged in the respective log folders for the taxis and passengers.

We can run the taxi system for a small number of taxis in our local machine, by making the following changes:
* Initialise no_of_taxis in ride_sharing.config to a small number (say 10, 20)
* Accordingly limit the no of rows in file (Each row indicates the initial position of the taxi) in 1dayNP_400taxis_Kmeans.csv (for NonPeak) or 1dayP_500taxis_Kmeans.csv (for Peak)
* Modify the no of passenger requests as needed in file Sun_NonPeak_passenger.csv present in folder TaxiSystem/NonPeakCode/Pass_Requests/ (for NonPeak) and modify Sun_Peak_passenger.csv present in folder TaxiSystem/PeakCode/Pass_Requests/ (for Peak)
* Run the below command to start the taxi system:
```
bash start.sh 2>&1 | tee full_op.txt
```

2. Queuing Model: Running the queueing model is similar to running the taxi system. In this module the requests are prioritised and then considered for computation by the taxi system.

3. Metrics: After running the taxi system, collect the results of each iteration and insert into the folder Iterations. A sample folder Iterations has been inserted. If the inserted folder is a zip then run extract.py to extract the folder and then run 

```
python3 metrics.py 
```

Doing this will display the average results over all iterations. The success rate of Nth passenger request and Nth acceptance will be plotted and saved in the base folder. The results for each iteration is inserted in the folder JSON. The success rate of Nth passenger for each iteration will be folder Cap and the Nth acceptance for all iterations is plotted and saved in folder Acceptance.

4. Pareto Analysis: Place the results of the taxi system in the respective NonPeak and Peak folders. Change the folder name in pareto_front.py based on whether minimum distance from origin was considered or utility function was considered while running the taxi system. After this, run the below command:

```
python3 pareto_front.py
```	

The graphs will be respectively plotted in the folders.

5. QueueLengthDistribution: The results from NonPeak and peak are placed in 400_60T_90P and 500_60T_90P folders. The data from queue_log folder is used in the computation, the results for these will be collected when we run the taxi system. The below command will find the start and end time at which the taxi system started and stopped.

```
python3 find_min_max.py
```

The below command will generate the list of all timings at an interval of 5 minutes from start time to end time.

```
python3 print_timelength.py
```

The below command will generate queue length distribution for non peak and peak hours respectively.

```
python3 queue_length_nonpeak.py
```

```
python3 queue_length_peak.py
```

The graphs for queue length distribution will be plotted in the respective folders.

