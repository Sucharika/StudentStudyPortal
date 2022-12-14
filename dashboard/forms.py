from re import L
from socket import fromshare
from django import forms 
from django.forms import ClearableFileInput
from dashboard.models import *



class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class stNotesForm(forms.ModelForm):
    class Meta:
        model = stNotes
        fields = ['category','title','description','files']
        widgets = {
            'media': ClearableFileInput(attrs={'multiple': True})
        }
        

class DateInput(forms.DateInput):
    input_type ='date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject','title','description','due','is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length = 100, label = "Enter your Search: ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices = CHOICES, widget = forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard','Yard'),('foot','Foot'),('meter','Meter')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '',
        widget = forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label = '',
        widget = forms.Select(choices = CHOICES)
    )

class ConversionMassForm(forms.Form):
    CHOICES = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '',
        widget = forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label = '',
        widget = forms.Select(choices = CHOICES)
    )

class noticeform(forms.ModelForm):
    class Meta:
        model = notice
        fields = ['title','description']