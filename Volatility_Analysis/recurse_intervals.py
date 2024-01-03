from standard_dev import standardDev
import pandas as pd
import numpy as np
from Input_Handeler import date_object


class recurse_interval:

    # Initialize main list
    def __init__(self, values):
        self.values = values

    # Recursive method
    def recurse(self, li):

        if len(li) > 0:
            # Calculate standard deviation
            volatility = standardDev(li).calculate_volatility()
            ending_index = int(len(li)/3)
            return volatility+self.recurse(li[0:ending_index])
        else:
            return 0

    # Call recursive function with initial values
    def call_recurse(self):
        # Interval volatility
        interval_1 = self.recurse(self.values[0: int(len(self.values)/4)])
        interval_2 = self.recurse(self.values[int(len(self.values)/4):int(len(self.values)/2)])
        interval_3 = self.recurse(self.values[int(len(self.values) /2): (int(3*len(self.values)/4))])
        interval_4 = self.recurse(self.values[(int(3*len(self.values)/4)):len(self.values)])

        print(f"Interval #1 = {interval_1}")
        print(f"Interval #2 = {interval_2}")
        print(f"Interval #3 = {interval_3}")
        print(f"Interval #4 = {interval_4}")

        return self.is_close(interval_1 + interval_2, interval_3 + interval_4)

    # Determine if two numbers are in  proximity
    def is_close(self, n1, n2):
        if abs(n1-n2) >= .4:
            return True
        return False


data = pd.read_csv('data.csv')
data = data["Close"]
col = np.array(data)
recurse_interval(col).call_recurse()

grapher = date_object.input_handler()
grapher.create_graph()
