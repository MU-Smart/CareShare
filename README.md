# CARE-Share: A Cooperative and Adaptive Strategy for Distributed Taxi Ride Sharing

In this project, we have modelled a distributed dynamic ride-sharing system as a multi-objective optimisation problem and solved it using the Ant Colony optimisation technique which sports a multi-agent behaviour. We have also explored the novel performance metrics to capture the underlying subtlety of the distributed system performance.

## Code Organisation

There are two folders, named **code** and **data**. Each has its own README.md file which has the details to run the code and the dataset respectively.

## Envirnoment Details

For simulating a full scale taxi system with large no of taxis, we can use any computing clusters. The experiments in this project were conducted on the computing cluster provided by Miami University with 2 compute nodes and 4 processors per node for running the experiments. pip3 and python3 needs to be installed on the computes. Some packages which needs to be installed for the simulating the experiment are : csv, flask, geojson, googlemaps, matplotlib, numpy, pandas, pickle, pprint, psutil, requests, scipy, sklearn.

In order to run the taxi system, we connected to the Miami cluster and then connect to the compute nodes using the below command:

```
qsub -l  nodes = 2:ppn = 4 -l walltime=9:00:00-IV -X
```

Here, nodes, ppn can be configured according to requirements. The value of walltime depends on the number of hours required to run the taxi system. After connecting to the compute node, go to the NonPeakCode or PeakCode folder (within the code/TaxiSystem folder) and run the below command to start the simulation for non-peak or peak hours respectively:

```
bash start.sh 2>&1 | tee full_op.txt
```

For simulating a small scale taxi system, please refer [here](https://github.com/MU-Smart/CareShare/tree/main/code#simulating-a-small-scale-taxi-system).
