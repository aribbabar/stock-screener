from django.http import HttpRequest
from django.shortcuts import redirect


def remove_duplicates(input_list):
    unique_list = []
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def logout_required(func):
    def inner(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("screener:index")

        func()

    return inner
