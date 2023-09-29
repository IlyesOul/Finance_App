import requests
import json
import csv
import datetime


class converter:

    # Initializes converter object and fields
    def __init__(self, url):
        r = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        self.r_json = r.json()
        self.ticker = self.r_json.get("chart").get("result")[0].get("meta").get("symbol")

    # Writes JSON data to CSV and JSON files
    def write_to_file(self, file_name_json, file_name_csv):
        # Writing to JSON file
        ticker = ""+self.ticker
        with open(file_name_json, "w") as outfile:
            json.dump(self.r_json, outfile)

        with open(file_name_json, encoding='utf-8') as f:
            data = json.loads(f.read())

        # Converting to CSV dataframe and writing
        header = ["Sticker", "Low", "Close", "High", "Open", "Volume", "Timestamp"]
        all_results = self.r_json.get("chart").get("result")[0].get("indicators").get("quote")[0]

        full_values = {"low": [],
                       "close": [],
                       "high": [],
                       "open": [],
                       "volume": [],
                       "timestamps": []}

        # Retrieving timestamps
        for item in self.r_json.get("chart").get("result")[0].get("timestamp"):
             full_values["timestamps"].append(item)

        # Filling the full_values dictionary with appropriate values
        for index in range(len(all_results.get("low"))):
            for curr_row in all_results:
                if curr_row != "timestamps":
                    full_values[curr_row].append(all_results.get(curr_row)[index])
            index += 1

        # Initializing and filling final 2d-array to write to file
        final_arr = []

        for index in range(len(full_values.get("volume"))):
            list_to_add = [ticker]
            for attribute in full_values:
                list_to_add.append(round(full_values.get(attribute)[index], 2))
            final_arr.append(list_to_add)

        # Writing final values to CSV file
        with open(file_name_csv, 'w') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(header)
            for index in range(len(final_arr)):
                csvwriter.writerow(final_arr[index])

    # Returns valid window ranges
    def get_valid_dates(self):
        dates = []

        for unix in self.r_json['chart']['result'][0]['timestamp']:
            date = datetime.datetime.fromtimestamp(unix)
            dates.append(date)

        return dates


# conv = converter('https://query1.finance.yahoo.com/v8/finance/chart/xom?period1=915166800&period2=1041397200&interval=1mo&includeAdjustedClose=false')
# conv.write_to_file('data.json', 'data.csv')
