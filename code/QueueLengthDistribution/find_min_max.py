import os
import json

d_all = []
fold = "./400_60T_90P/queue_log/"
for fld in os.listdir(fold):
	print(fld)
	with open(fold+fld) as f:
		d = json.load(f)
	print(d["queue"])
	for i in d["queue"]:
		d_all.append(i["timestamp"])


print(len(d_all),max(d_all),min(d_all))
