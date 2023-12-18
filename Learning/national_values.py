import pandas as pd
from Data_Conversion import convert
import csv
import numpy as np
import requests
import numbers
from sklearn.linear_model import LinearRegression
import datetime


class economy_correlations:

	# Initialize converter object and write to file
	def __init__(self):
		print("Start date MUST be Jan 1st 2007")
		# Initialize JSON query link and create converter-object with it
		date = datetime.datetime(2007, 1, 1)
		unix_timestamp_1 = datetime.datetime.timestamp(date)
		date = datetime.datetime(2022, 12, 1)
		unix_timestamp_2 = datetime.datetime.timestamp(date)
		print()
		print()
		stock_name = input("What is the ticker of the desired stock?")
		initialized_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_name.lower()}?period1={str(int(unix_timestamp_1))}&period2={str(int(unix_timestamp_2))}&interval=1d&includeAdjustedClose=false"
		print(initialized_url)
		self.converter = convert.converter(initialized_url)
		self.converter.write_to_file('training.json', 'training.csv')

	# Obtain data
	def obtain_data_from_files(self):
		# Write appropriate data to file
		open_values = self.converter.get_feature_values("open")

		if len(open_values) > 192:
			open_values = open_values[:192]

		header = ["Open", "Forex", "Inflation", "Interest"]

		# Write stock opening values
		with open('national_factors.csv', 'w') as f:
			# Write header row
			writer = csv.writer(f)
			writer.writerow(header)

			# Dictionary of all values
			all_values = {
				"Open": open_values[:192],
				"Forex": [],
				"Inflation": [],
				"Interest": []
			}

			# Obtain interest rates from 'interest_rates' file and append to 'all_values' array
			rates_file = pd.read_csv('interest_rates')
			all_values["Interest"] = np.array(rates_file["Rates"])

			# Obtain inflation rates from 'inflation_rates' and append to 'all_values' array
			rates_file = pd.read_csv('inflation_rates')
			all_values["Inflation"] = np.array(rates_file["Rates"])

			# Obtain currency values from Forex API
			forex_open = []
			# Downloads CSV-formatted file of Forex rates
			forex_JSON = requests.get("https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&apikey=2RP8A05B6JJ2RP71&datatype=csv")

			# Open downloaded CSV file
			with open("C:/Users/ouibr/Downloads/fx_monthly_EUR_USD.csv") as fi:
				reader = csv.reader(fi)
				# Fill 'forex_open' array with open values
				for row in reader:
					if row[1] != "open":
						all_values["Forex"].append(float(row[1]))
				all_values["Forex"] = all_values["Forex"][:192]

			# Final 2D-Array to write to CSV file
			writable_values = []
			list_to_add = []

			for index in range(len(all_values.get("Open"))):
				list_to_add = []
				for attribute in all_values:
					if isinstance(all_values.get(attribute)[index], numbers.Number):
						list_to_add.append(round(float(all_values.get(attribute)[index]), 2))
				writable_values.append(list_to_add)

			# Writing final values to CSV file
			csvwriter = csv.writer(f)
			for index in range(len(writable_values)):
				csvwriter.writerow(writable_values[index])

			# Train and test model on procured data

		# Attain training and testing data
		data = pd.read_csv('national_factors.csv')
		x = np.array(data.drop(["Open"], 1))
		y = np.array(data["Open"])

		# Train-test data split
		train_x = x
		train_y = y

		test_x = x[20:]
		test_y = y[20:]

		# Fit and test data with Linear Regression Model
		log = LinearRegression()
		log.fit(train_x, train_y)

		result_dict = log.predict(test_x)

		print(f"Accuracy = {log.score(test_x, test_y)}")


object = economy_correlations()
object.obtain_data_from_files()
