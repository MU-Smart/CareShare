import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt


def get_success_rate(file_name_p):
	df = pd.read_csv(file_name_p)

	df = pd.DataFrame(df)

	failures = df.isna().sum().sum()/5


	rate = (df.shape[0] - failures)/ df.shape[0]

	sucess = (df.shape[0] - failures)

	return sucess,rate
