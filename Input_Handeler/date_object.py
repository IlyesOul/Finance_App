import datetime
from Data_Conversion import convert
import pandas as pd
import matplotlib.pyplot as plt


class input_handler:

	# Constructor
	def __init__(self):
		# Date field values
		self.day = 0
		self.month = 0
		self.year = 0

	# Prompts user for date-values
	def prompt_date(self):
		self.day = int(input("What is the day? (Start with 0 if single-digit) "))
		self.month = int(input("What is the month? (Start with 0 if single-digit) "))
		self.year = int(input("What is the year? "))

	# Returns unix_formatted date
	def to_unix(self):
		date2 = datetime.datetime(self.year, self.month, self.day)
		unix_timestamp = datetime.datetime.timestamp(date2)
		return str(int(unix_timestamp))

	# Initializes and returns an API request URL
	def initialize_url(self):
		name = input("What is the name of your stock? ")
		print("This is the starting interval: ")
		self.prompt_date()
		unix_1 = self.to_unix()
		print("This is the ending interval: ")
		self.prompt_date()
		unix_2 = self.to_unix()

		return f'https://query1.finance.yahoo.com/v8/finance/chart/{name.lower()}?period1={unix_1}&period2={unix_2}&interval=1d&includeAdjustedClose=false'

	# Graph a base JSON query
	def create_graph(self):
		converter = convert.converter(self.initialize_url())
		converter.write_to_file('data.json', 'data.csv')

		data = pd.read_csv("data.csv")
		data = data["Close"]
		values = []

		for val in data:
			values.append(val)

		# Graph data

		plt.plot(converter.get_valid_dates(), values, c='blue')

		plt.title("Close - Daily", fontsize=14)
		plt.xlabel("Dates", fontsize=15)

		label = "$ USD"

		plt.ylabel(label.upper(), fontsize=15)

		plt.show()
