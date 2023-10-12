from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import hostel_details, transactions
from django.contrib.auth.models import User
from django.template import loader

room = ""

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
        form_type = request.POST.get("form_type", "")
        if form_type == "booking":
            hostel_block = request.POST["hostel_block"]
            cooling = request.POST["cooling"]
            sharing = request.POST["sharing"]
            bathroom = request.POST["bathroom"]
            # print(hostel_block, cooling, sharing, bathroom, end="\n")
            room = hostel_details.objects.filter(block=hostel_block,
                                                cooling=cooling,
                                                sharing=sharing,
                                                bathroom=bathroom).values()[0]
    
        elif form_type == "payment":
            room_id = request.POST["room_id"]
            print(request.user)
            transaction = transactions(user=request.user, room_id=room_id)
            transaction.save()
            return HttpResponseRedirect(reverse("transaction"))


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

def transaction(request):
    try:
        username = request.user
        transactions_obj = transactions.objects.filter(user=username).values()[0]
        room_id = transactions_obj["room_id"]
        room_details = hostel_details.objects.filter(id=room_id).values()[0]
        print(room_details)
        return render(request, "booking/transaction.html", {"room_details": room_details})
    except:
        return render(request, "booking/transaction.html")