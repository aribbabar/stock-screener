from django.http import HttpRequest
from django.shortcuts import redirect


def remove_duplicates(input_list):
    unique_list = []
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def format_large_number(number):
    if number < 1e6:
        return str(number)
    elif number < 1e9:
        return f"{number / 1e6: .1f}M"
    elif number < 1e12:
        return f"{number / 1e9: .1f}B"
    elif number < 1e15:
        return f"{number / 1e12: .1f}T"
    else:
        return str(number)


def logout_required(func):
    def inner(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("screener:index")

        return func(request, *args, **kwargs)

    return inner
