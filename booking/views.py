from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


# Create your views here.
def index(request):
    current_user = request.user
    context = {
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
    }
    return render(request, "booking/index.html", context)


"""
if request.user.is_authenticated:
    # Do something for authenticated users.
else:
    # Do something for anonymous users.
"""