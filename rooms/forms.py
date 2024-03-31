from django import forms
from datetime import date
from .models import Reservation


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


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        widgets = {
            'check_in': DateInput(attrs={'min': date.today()}),
            'check_out': DateInput(attrs={'min': date.today()})
        }

