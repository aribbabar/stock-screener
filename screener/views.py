import requests
from bs4 import BeautifulSoup
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
    URL = "https://finance.yahoo.com/quote/" + symbol

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    stock_id = Stock.objects.filter(symbol=symbol)[0].id
    stock_name = soup.find(name="h1", class_="D(ib) Fz(18px)").text
    stock_price = soup.find(name="fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)",
                            attrs={"data-field": "regularMarketPrice"}).text
    stock_change_value = soup.find(name="fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)", attrs={
                                   "data-field": "regularMarketChange"}).findChild("span").text
    stock_change_percent = soup.find(name="fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)", attrs={
                                     "data-field": "regularMarketChangePercent"}).findChild("span").text

    context = {
        "stock_id": stock_id,
        "stock_name": stock_name,
        "stock_price": stock_price,
        "stock_change_value": stock_change_value,
        "stock_change_percent": stock_change_percent
    }

    # context = {
    #     "stock_id": stock_id,
    #     "stock_name": "Meta Platforms, Inc. (META)",
    #     "stock_price": "321.15",
    #     "stock_change_value": "+6.46",
    #     "stock_change_percent": "(+2.05%)"
    # }

    if request.user.is_authenticated:
        user_id = request.user.id
        stock_id = Stock.objects.filter(symbol=symbol)[0].id

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
                print("Invalid username/password", user)

    return render(request, "screener/login.html", {"form": form})


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
