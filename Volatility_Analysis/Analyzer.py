from Data_Conversion import convert
from recurse_intervals import recurse_interval
import pandas as pd


class volatilityAnalyzer:

    def __init__(self, url):
        self.conversion = convert.converter(url)
        self.write_to_file()

    def write_to_file(self):
        self.conversion.write_to_file("data.json", "data.csv")

    def calculate_volatility(self, attribute):

        # Get data column
        data = pd.read_csv("data.csv")
        column = data[attribute.title()]

        # Get volatility from stdev class
        volatility_obj = recurse_interval(column)
        return volatility_obj.call_recurse()

