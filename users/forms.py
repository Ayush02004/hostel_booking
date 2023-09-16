from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", 'email', 'password1', 'password2')

"""
class UserRegisterForm(UserCreationForm):
    registration_no = forms.CharField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", 'username', 'registration_no', 'email', 'password1', 'password2')
"""

"""
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    username = forms.

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'registration_no', 'email', 'password1', 'password2')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=100)
    reg_no = forms.CharField(max_length=16)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
"""