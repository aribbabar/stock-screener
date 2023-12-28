import requests
from bs4 import BeautifulSoup

URL = "https://finance.yahoo.com/quote/META"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

stock_name = soup.find(name="h1", class_="D(ib) Fz(18px)").text
stock_price = soup.find(name="fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)",
                        attrs={"data-field": "regularMarketPrice"}).text
stock_change_value = soup.find(name="fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)",
                               attrs={"data-field": "regularMarketChange"}).findChild("span").text
stock_change_percent = soup.find(name="fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)", attrs={
                                 "data-field": "regularMarketChangePercent"}).findChild("span").text
previous_close = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
                           "data-test": "PREV_CLOSE-value"}).text
open = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "OPEN-value"}).text
bid = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "BID-value"}).text
ask = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "ASK-value"}).text
days_range = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "DAYS_RANGE-value"}).text
fifty_two_week_range = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "FIFTY_TWO_WK_RANGE-value"}).text
volume = soup.find(name="fin-streamer",
                   attrs={"data-field": "regularMarketVolume"})["value"]
average_volume = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "AVERAGE_VOLUME_3MONTH-value"}).text
market_cap = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
                       "data-test": "MARKET_CAP-value"}).text
beta = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "BETA_5Y-value"}).text
pe_ratio = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "PE_RATIO-value"}).text
eps = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "EPS_RATIO-value"}).text
earnings_date = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "EARNINGS_DATE-value"}).text
one_year_target = soup.find(name="td", class_="Ta(end) Fw(600) Lh(14px)", attrs={
    "data-test": "ONE_YEAR_TARGET_PRICE-value"}).text

print(stock_name, stock_price, stock_change_value, stock_change_percent, previous_close, open, bid, ask, days_range, fifty_two_week_range,
      volume, average_volume, market_cap, beta, pe_ratio, eps, earnings_date, one_year_target)
