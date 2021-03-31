import pandas as pd
import csv
df = pd.read_csv("Sun_Peak_passenger-duplicates.csv")
ct = 0
for i,row in df.iterrows():
	print(i)
	with open("Sun_Peak_passenger.csv","a") as results_file:
			row_temp = [row[0],row["dropoff_latitude"],row["dropoff_longitude"],row["pickup_latitude"],row["pickup_longitude"],row["time"]]
			print(row_temp)
			csv_writer = csv.writer(results_file)
			csv_writer.writerow(row_temp)
	results_file.close()
