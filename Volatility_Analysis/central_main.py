from Analyzer import volatilityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os

# Analyzer Object
volatilityAnalyzer

# Date field values
day = 0
month = 0
year = 0

# Period
period = ""

# Dates for plotting
dates = []


# Prompts user for date-values
def prompt_date():
    global day
    day = int(input("What is the day? (Start with 0 if single-digit) "))
    global month
    month = int(input("What is the month? (Start with 0 if single-digit) "))
    global year
    year = int(input("What is the year? "))


# Returns unix_formatted date
def to_unix():
    date2 = datetime.datetime(year, month, day)
    unix_timestamp = datetime.datetime.timestamp(date2)
    return str(int(unix_timestamp))


# Initializes and returns an API request URL
def initialize_url(period):
    name = input("What is the name of your stock? ")
    print("This is the starting interval: ")
    prompt_date()
    unix_1 = to_unix()
    print("This is the ending interval: ")
    prompt_date()
    unix_2 = to_unix()

    return f'https://query1.finance.yahoo.com/v8/finance/chart/{name.lower()}?period1={unix_1}&period2={unix_2}&interval={period}&includeAdjustedClose=false'


# Returns volatility float
def return_volatility(url, attr):
    print(url)

    global volatilityAnalyzer
    analyzer = volatilityAnalyzer(url)

    # Write info to file and retrieve volatility
    analyzer.write_to_file()

    global dates
    dates = analyzer.conversion.get_valid_dates()

    # Retrieve and return volatility
    volatility = analyzer.calculate_volatility(attribute=attr)
    return volatility


def determine_results(attr):
    # Initialize URLs
    periods = ["60m", "1d", "5d", "1wk", "1mo", "3mo"]
    print(f"Valid periods: {periods}")
    print("Note: If you select a minute-interval, the time must be within the previous 730 days")

    # Period value
    global period
    period = input("What is the period you would like to see? ")
    day_url = initialize_url(period)

    # Initialize volatilities
    day_v = return_volatility(day_url, attr)
    print(f"Volatility = {day_v}")
    display_graph(day_url, attr)


def display_graph(url, attr):

    # Collect attribute data
    data = pd.read_csv("data.csv")
    data = data[attr.title()]
    values = []

    for val in data:
        values.append(val)

    # Graph data
    global dates
    plt.plot(dates, values, c='blue')

    plt.title(f"{attr.title()} - {period}", fontsize=14)
    plt.xlabel("Dates", fontsize=15)

    label = "$ USD"
    if attr.upper() == "VOLUME":
        label = "Shares Sold (Number * e +10)"

    plt.ylabel(label.upper(), fontsize=15)

    plt.show()
    try:
        os.remove('plotted_graph.jpeg')
    except OSError as e:
        print(f"Error: {e}")
    plt.savefig('plotted_graph.jpeg', format='jpeg')


att = input("What do you want to calculate volatility for? ")
determine_results(att)
