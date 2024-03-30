from django import forms
from datetime import date


class DateInput(forms.DateInput):
    input_type = 'date'


class DateForm(forms.Form):
    sort_choices = [
        ('asc', 'Возрастанию цены'), ('desc', 'Убыванию цены'), ('number', 'По номеру комнаты')
    ]

    cin = forms.DateField(widget=DateInput(attrs={'min': date.today()}), initial=None, required=False, label='Заезд')
    cout = forms.DateField(widget=DateInput(attrs={'min': date.today()}), initial=None, required=False, label='Выезд')
    person = forms.IntegerField(label="Количество гостей")
    sort = forms.ChoiceField(
        choices=sort_choices,
        widget=forms.Select(attrs=
                            {"class": "form-control"}), initial=None, required=False, label='Сортировать по')
