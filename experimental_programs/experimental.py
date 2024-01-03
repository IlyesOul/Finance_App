import requests
import re
from bs4 import BeautifulSoup
import yfinance as yf


# Retrieve name based on ticker
def get_name(ticker):
    url = f"https://api.polygon.io/v3/reference/tickers/{ticker.upper()}?apiKey=VFSwKNWbH7pv7Yp98ayguccA6KVAJYjr"
    request_json = requests.get(url).json()

    return request_json["results"]["name"]


# Return a prepared URL for site-scrapping
def google_query(search_term):
    if "news" not in search_term:
        search_term = search_term+" stock news"
    url = f"https://www.google.com/search?q={search_term}&rlz=1C1CHBF_enUS968US968&oq={search_term}+stock+news&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg7MgYIAhBFGEDSAQgxOTIzajBqN6gCALACAA&sourceid=chrome&ie=UTF-8"
    url = re.sub(r"\s", "+", url)
    return url


# Returns list of top 5 stock news articles related to that company
def get_recent_stock_news(company_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    # JSON Request
    g_query = google_query(company_name)
    print(g_query)
    res = requests.get(g_query, headers=headers).text

    # Scrap google site for appropriate div tags
    soup = BeautifulSoup(res, "html.parser")
    news = []
    for n in soup.find_all("div", "n0jPhd ynAwRc tNxQIb nDgy9d"):
        news.append(n.text)
    for n in soup.find_all("div", "IJl0Z"):
        news.append(n.text)
    if len(news) > 6:
        news = news[:5]

    # Append yahoo-finance articles to news
    company = yf.Ticker(company_name)
    news_json = company.news

    for index in range(5):
        if index <= 5:
            news.append(news_json[index]["title"])
    return news


def experimental(ticker):
    company = yf.Ticker(ticker)

    # Related Companies
    related_companies = company.news[len(company.news)-1]["relatedTickers"]
    print(f"Related = {related_companies}")

    # Top 5 institutional investors
    top_5 = company.institutional_holders[:5]
    print(f"Top 5 = {top_5}")

    # Balance sheet
    balance_sheet = company.balancesheet
    print(f"Balance sheet = {balance_sheet}")

    # Financials and cashflow
    cashflow = company.cash_flow
    print(f"Cashflow = {cashflow}")
    financials = company.financials
    print(f"Financials = {financials}")


comp_ticker = input("What is your ticker? ")
print(f"Stock News: {get_recent_stock_news(company_name=comp_ticker)}")
# experimental(comp_ticker)
# print(get_name(comp_ticker))
