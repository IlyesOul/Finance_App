import statistics
import math


class standardDev:

    # Constructor
    def __init__(self, values):
        self.values = values

    def calculate_volatility(self):
        # Collect parameter
        values = self.values
        mean = statistics.mean(values)
        divs = []
        for value in values:
            divs.append(value-mean)

        sum_1 = 0
        for value in divs:
            sum_1 += value**2

        # Return Standard Deviation
        return (math.sqrt(sum_1/len(values))/len(values))
