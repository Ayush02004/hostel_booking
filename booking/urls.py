from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("details", views.details, name="details"),
    path("booking", views.booking, name="booking"),
    path("transaction", views.transaction, name="transaction"),
]
