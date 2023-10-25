from Data_Conversion import convert
import numpy as np
import pandas as pd
import matplotlib.pyplot as mp


class moving_average_analyzer:
    def __init__(self, dat):
        self.data = dat

    # Calculates and returns the SMA
    def simple_moving_average(self, n):
        if n == 0:
            return self.data[0]
        else:
            ret = 0
            for val in range(n+1):
                ret += val
            return ret

    # Calculates and returns the EMA
    def exponential_moving_average(self, n):
        past_ema = 0
        if n == 0:
            past_ema = self.simple_moving_average(n)
        else:
            past_ema = self.exponential_moving_average(n-1)

        k = 2/(n+1)
        return k*(self.data[n] - past_ema)+past_ema




converter = convert.converter("https://query1.finance.yahoo.com/v8/finance/chart/aapl?period1=1609477200&period2=1672549200&interval=1mo&includeAdjustedClose=false")
data = pd.read_csv('data.csv')
arr = np.array(data["Close"])
analyzer = moving_average_analyzer(arr)
values = []
for index in range(len(arr)):
    values.append(analyzer.exponential_moving_average(index))

indexes = list(i for i in range(len(arr)))
mp.plot(indexes, arr, label="values")
mp.plot(indexes, values, label="EMA")
mp.legend()
mp.show()
