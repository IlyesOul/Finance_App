import csv
from sklearn.ensemble import RandomForestRegressor
from Data_Conversion import convert
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Input_Handeler import date_object

# File is filled with appropriate data
# Initialize JSON query link and create converter-object with it
initialized_url = date_object.input_handler().initialize_url()
converter = convert.converter(initialized_url)

converter.write_to_file("training.json", "aux_file.csv")


data = []
first_row = []

# Preprocessing data
with open("training.csv", 'r', newline='') as csvfile:
	reader = csv.reader(csvfile)
	first_row = next(reader)
	first_row = first_row[1:]
	digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	for row in reader:
		converted_row = []
		for value in row:
			if "0" in value or "1" in value or "2" in value or "3" in value or "4" in value or "5" in value or "6" in value \
					or "7" in value or "8" in value or "9" in value:
				converted_row.append(int(float(value)))
		data.append(converted_row)

# Write final data to CSV file
with open("aux_file.csv", 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(first_row)
	for row in data:
		writer.writerow(row)

# Import and preprocess data
data = pd.read_csv("aux_file.csv")

x = np.array(data.drop(["High"], 1))
y = np.array(data["High"])

# Create training and testing data samples
train_x = x[len(x)-250:len(x)-50:]
train_y = y[len(x)-250:len(y)-50]

test_x = x[len(x)-50:]
test_y = y[len(y)-50:]

# Initialize pre-pruned Random Forest Ensemble
forest = RandomForestRegressor(max_leaf_nodes=12, n_estimators=25, n_jobs=-1)

# Train forest
forest.fit(train_x, train_y)

# Predicted values
predicted_values = np.array(forest.predict(test_x))
score = forest.score(test_x, test_y)

# Collect attribute data
data = pd.read_csv("training.csv")
dates = data["Timestamp"]
data = data["Open"]
values = []

for val in data:
	values.append(val)

# Graph data
plt.plot(dates, values, c='blue', label="Historical Value")

dates = dates[len(x)-50:]
plt.plot(dates, predicted_values, c="yellow", label="Predicted Value")

plt.title(f"Daily Open", fontsize=14)
plt.xlabel("Dates", fontsize=15)
plt.ylabel("$ USD", fontsize=15)


plt.legend()
plt.show()

