from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class PersonRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password']

class EditRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class PersonLogin(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password']


    