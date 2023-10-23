import requests
from bs4 import BeautifulSoup

URL = "https://finance.yahoo.com/quote/META"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

stock_name = soup.find(name="h1", class_="D(ib) Fz(18px)").text
stock_price = soup.find(name="fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)", attrs={"data-field": "regularMarketPrice"}).text
stock_change_value = soup.find(name="fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)", attrs={"data-field": "regularMarketChange"}).findChild("span").text
stock_change_percent = soup.find(name="fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)", attrs={"data-field": "regularMarketChangePercent"}).findChild("span").text

print(stock_name, stock_price, stock_change_value, stock_change_percent)