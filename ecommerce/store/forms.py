from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django import forms
from django.db.models import fields
from django.db.models.base import Model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2','email']


class CreateAddressForm(forms.ModelForm):
    class Meta:
        model = ShoppingAddress
        fields = ['state','zipcode','city','address']