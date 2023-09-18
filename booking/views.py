from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import hostel_details


def index(request):
    if not request.user.is_authenticated:
        # current_user = request.user
        return HttpResponseRedirect(reverse("login"))
    # temp = hostel_details.objects.all()
    # print(temp)
    return render(request, "booking/index.html")


def details(request):
    room_details = hostel_details.objects.all()
    return render(request, "booking/details.html", {"room_details": room_details})