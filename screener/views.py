
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render

from screener.forms import LoginForm, RegisterForm

from .models import Stock, UserStock
from .utils import logout_required, remove_duplicates


def index(request: HttpRequest):
    return render(request, "screener/index.html")


def stock_info(request: HttpRequest, symbol: str):
    stock_url = f"https://finance.yahoo.com/quote/{symbol}"
    page = requests.get(stock_url)

    if page.status_code == 404:
        return render(request, "screener/404.html")

    soup = BeautifulSoup(page.content, "html.parser")

    stock_id = Stock.objects.get(symbol=symbol).id
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

    context = {
        "stock_id": stock_id,
        "stock_name": stock_name,
        "stock_price": stock_price,
        "stock_change_value": stock_change_value,
        "stock_change_percent": stock_change_percent,
        "previous_close": previous_close,
        "open": open,
        "bid": bid,
        "ask": ask,
        "days_range": days_range,
        "fifty_two_week_range": fifty_two_week_range,
        "volume": volume,
        "average_volume": average_volume,
        "market_cap": market_cap,
        "beta": beta,
        "pe_ratio": pe_ratio,
        "eps": eps,
        "earnings_date": earnings_date,
        "one_year_target": one_year_target
    }

    # context = {
    #     "stock_id": "1",
    #     "stock_name": "AAPL",
    #     "stock_price": "173.00",
    #     "stock_change_value": "+0.12",
    #     "stock_change_percent": "(+0.07%)",
    #     "previous_close": "172.88",
    #     "open": "170.91",
    #     "bid": "172.93 x 1100",
    #     "ask": "173.01 x 1000",
    #     "days_range": "169.94 - 174.01",
    #     "fifty_two_week_range": "124.17 - 198.23",
    #     "volume": "55,856,506",
    #     "average_volume": "58,053,110",
    #     "market_cap": "2.705T",
    #     "beta": "1.31",
    #     "pe_ratio": "29.03",
    #     "eps": "5.96",
    #     "earnings_date": "Nov 02, 2023",
    #     "forward_dividend_and_yield": "0.96 (0.56%)",
    #     "ex_dividend_date": "Aug 11, 2023",
    #     "target_mean": "187.73"
    # }

    if request.user.is_authenticated:
        user_id = request.user.id

        if UserStock.objects.filter(user=user_id).filter(stock=stock_id):
            context["stock_exists"] = True

    return render(request, "screener/stock_info.html", context)


@login_required
def add_stock(request: HttpRequest, stock_id):
    user = request.user
    stock = Stock.objects.get(pk=stock_id)

    if "add" in request.POST:
        new_stock = UserStock(user=user, stock=stock)
        new_stock.save()
    elif "remove" in request.POST:
        UserStock.objects.get(user=user, stock=stock).delete()

    return redirect("screener:my_stocks")


def search(request: HttpRequest, search_term: str):
    # Get the first 5 values where the stock symbol matches the search term
    symbols = Stock.objects.filter(symbol__contains=search_term).values()[:5]
    formatted_results = [
        f"{entry['symbol']} | {entry['security_name']}" for entry in symbols]

    # If there were less than 5 results from the query above, get the next 5 values where the security's name matches the search term
    if len(symbols) < 5:
        security_names = Stock.objects.filter(
            security_name__contains=search_term).values()[:5]
        formatted_results = formatted_results + \
            [f"{entry['symbol']} | {entry['security_name']
                                    }" for entry in security_names]
        # to remove duplicates while maintaing the order
        formatted_results = remove_duplicates(formatted_results)

    return JsonResponse({"data": formatted_results})


@logout_required
def register(request: HttpRequest):
    form = RegisterForm()

    if request.method == "POST":
        User = get_user_model()
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            User.objects.create_user(username=username, email=email,
                                     password=password, first_name=first_name, last_name=last_name)

            messages.add_message(request, messages.SUCCESS,
                                 "Account created successfully!")

            return redirect("screener:login")
        else:
            print(form.errors)

    return render(request, "screener/register.html", {"form": form})


@logout_required
def login(request: HttpRequest):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                return redirect("screener:index")
            else:
                messages.add_message(request, messages.ERROR,
                                     "Invalid username/password")
                print("Invalid username/password", user)

    return render(request, "screener/login.html", {"form": form})


@login_required
def logout(request: HttpRequest):
    if request.user.is_authenticated:
        auth_logout(request)

    return redirect("screener:index")


@login_required(login_url="/login")
def my_stocks(request: HttpRequest):
    user_id = request.user.id
    user_stocks = UserStock.objects.filter(user=user_id)

    stocks = []

    for stock in user_stocks:
        stocks.append(stock.stock)

    return render(request, "screener/my_stocks.html", {"user_stocks": stocks})
