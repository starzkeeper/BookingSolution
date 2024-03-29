from django import forms
from datetime import date


class DateInput(forms.DateInput):
    input_type = 'date'


class DateForm(forms.Form):
    cin = forms.DateField(widget=DateInput(attrs={'min': date.today()}), initial=date.today())
    cout = forms.DateField(widget=DateInput(attrs={'min': date.today()}), initial=date.today())
    person = forms.IntegerField()
