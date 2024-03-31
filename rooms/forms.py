from django import forms
from datetime import date
from .models import Reservation


class DateInput(forms.DateInput):
    input_type = 'date'


class DateForm(forms.Form):
    sort_choices = [
        ('asc', 'Возрастанию цены'), ('desc', 'Убыванию цены'), ('number', 'По номеру комнаты')
    ]

    check_in = forms.DateField(widget=DateInput(attrs={'min': date.today()}), initial=None, required=False, label='Заезд')
    check_out = forms.DateField(widget=DateInput(attrs={'min': date.today()}), initial=None, required=False, label='Выезд')
    guests = forms.IntegerField(label="Количество гостей", initial=1)
    sort = forms.ChoiceField(
        choices=sort_choices,
        widget=forms.Select(attrs=
                            {"class": "form-control"}), initial=None, required=False, label='Сортировать по')


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        widgets = {
            'check_in': DateInput(attrs={'min': date.today()}),
            'check_out': DateInput(attrs={'min': date.today()})
        }

