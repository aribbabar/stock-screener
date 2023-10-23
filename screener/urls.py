from django.urls import path

from . import views

app_name = "screener"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:search_term>", views.search),
    path("stock_info/<str:symbol>", views.stock_info, name="stock_info"),
    path("stock_info/add_stock/<str:stock_id>",
         views.add_stock, name="add_stock"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("my_stocks/", views.my_stocks, name="my_stocks")
]
