from Analyzer import volatilityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os
import numpy as np
from Pattern_Analyzer import recursive_analyzer


class main_t:

    def __init__(self, att):
        # Analyzer Object
        self.analyzer = volatilityAnalyzer(
            "https://query1.finance.yahoo.com/v8/finance/chart/aapl?period1=978325200&period2=1672"
            "549200&interval=1mo&includeAdjustedClose=false")

        # Date field values
        self.day = 0
        self.month = 0
        self.year = 0

        # Dates for plotting
        self.dates = []

        # Attribute
        self.attr = att

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

    # Returns volatility float
    def return_volatility(self, url):
        print(url)

        # Retrieve and return volatility
        volatility = self.analyzer.calculate_volatility(attribute=self.attr)
        return volatility

    def initialize(self):

        # Initialize URL
        day_url = self.initialize_url()

        self.analyzer = volatilityAnalyzer(day_url)

        # Write info to file and retrieve volatility
        self.analyzer.write_to_file()

        # Initialize correct dates
        global dates
        dates = self.analyzer.conversion.get_valid_dates()

        decision = int(input("Would you like to (0) graph, (1) volatility, (2) patterns? "))

        if decision == 0:
            self.display_graph(day_url)
        elif decision == 1:
            volatility = self.return_volatility(day_url)
        elif decision == 2:
            # Calculate patterns
            self.retrieve_patterns()

    def display_graph(self, url):
        print(url)

        # Collect attribute data
        data = pd.read_csv("data.csv")
        data = data[self.attr.title()]
        values = []

        for val in data:
            values.append(val)

        # Graph data
        global dates
        plt.plot(dates, values, c='blue')

        plt.title(f"{self.attr.title()} - Daily", fontsize=14)
        plt.xlabel("Dates", fontsize=15)

        label = "$ USD"
        if self.attr.upper() == "VOLUME":
            label = "Shares Sold (Number * e +10)"

        plt.ylabel(label.upper(), fontsize=15)

        plt.show()
        try:
            os.remove('plotted_graph.jpeg')
        except OSError as e:
            print(f"Error: {e}")
        plt.savefig('plotted_graph.jpeg', format='jpeg')

    # Retrieve patterns
    def retrieve_patterns(self):
        data = pd.read_csv("data.csv")
        arr = np.array(data[self.attr.title()])

        analyzer_w = recursive_analyzer.analyzer(arr, 0, len(arr) - 1)
        analyzer_w.return_patterns()
        print(analyzer_w.aux_list)


att = input("What attribute would you like to analyze? ")
instantiated = main_t(att)
instantiated.initialize()
