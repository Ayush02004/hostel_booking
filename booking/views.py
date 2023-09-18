from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import hostel_details, transactions
from django.contrib.auth.models import User
from django.template import loader


def index(request):
    # temp = hostel_details.objects.all()
    # print(temp)
    return render(request, "booking/index.html")


def details(request):
    room_details = hostel_details.objects.all()
    return render(request, "booking/details.html", {"room_details": room_details})


def booking(request):
    template = loader.get_template("booking/booking.html")
    room = ""
    if request.method == "POST":
        hostel_block = request.POST["hostel_block"]
        cooling = request.POST["cooling"]
        sharing = request.POST["sharing"]
        bathroom = request.POST["bathroom"]
        # print(hostel_block, cooling, sharing, bathroom, end="\n")
        room = hostel_details.objects.filter(block=hostel_block,
                                               cooling=cooling,
                                               sharing=sharing,
                                               bathroom=bathroom).values()[0]
    # try:
    #     payment = request.POST["payment"]
    #     print(payment)
    # except:
    #     pass

    block, cooling, sharing, bathroom = set(), set(), set(), set()
    for x in hostel_details.objects.all():
        block.add(x.block)
        cooling.add(x.cooling)
        sharing.add(x.sharing)
        bathroom.add(x.bathroom)
    # print(block, cooling, sharing, bathroom, end="\n")

    context = {
        "room": room,
        "hostel_block": block,
        "cooling": cooling,
        "sharing": sharing,
        "bathroom": bathroom,
    }

    return HttpResponse(template.render(context, request))

# def payment(request):
#     if request.method == "POST":
#         payment = request.POST["payment"]
#         username = request.user