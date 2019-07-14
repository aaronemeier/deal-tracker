from django.shortcuts import render


"""
    TODO: Add favicon
    TODO: logo
"""

def home(request):
    data = {

    }
    return render(request, "home.html", data)
