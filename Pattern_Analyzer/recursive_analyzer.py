import numpy as np
import pandas as pd
from Data_Conversion import convert
import statistics


class analyzer:
    def __init__(self, values, i1, i2):
        self.values = values
        self.i1 = i1
        self.i2 = i2
        self.hashmap = {}
        self.aux_list = {}

    # List is now filled with intervals and their differences
    def return_patterns(self):
        arr = self.values
        # Allocate the interval-periods
        big_n = int(input("How do you want the stock to be divided up (provide an integer): "))
        local_extrema = []
        for n in range(1, big_n+1):
            # Find the most deviant local extrema based off its difference from the mean reversion line
            if n == 1:
                local_extrema.append(min(arr[:round((n/big_n)*len(arr))+1]))
                local_extrema.append(max(arr[:round((n/big_n)*len(arr))+1]))
            else:
                index_1 = int(((n-1)/big_n)*(len(arr)))
                index_2 = round((n/big_n)*len(arr))-1
                print(f"Index_1 = {index_1}")
                print(f"Index_2 = {index_2}")
                print(f"n is {n}")
                local_extrema.append(min(arr[index_1:index_2]))
                local_extrema.append(max(arr[index_1:index_2]))
        self.aux_list = local_extrema


# converts = convert.converter('https://query1.finance.yahoo.com/v8/finance/chart/aapl?period1=978325200&period2=1672549200&interval=1mo&includeAdjustedClose=false')
# data = pd.read_csv('data.csv')
# arr = np.array(data["Close"])
# analyze = analyzer(arr, 0, len(arr))
# analyze.return_patterns()
# print(analyze.aux_list)
