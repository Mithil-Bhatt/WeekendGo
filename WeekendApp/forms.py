from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class stufrom(forms.ModelForm):
    class Meta:
        model=college
        fields='__all__'

class pgform(forms.ModelForm):
    class Meta:
        model=pg
        fields='__all__'


class ownerform(forms.ModelForm):
    class Meta:
        model=owner
        fields='__all__'

class feedbackdorm(forms.ModelForm):
    class Meta:
        model=feedback
        fields='__all__'


class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = '__all__'
