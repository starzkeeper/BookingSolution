from datetime import date

import django_filters
from django_filters.filterset import BaseFilterSet

from .forms import DateInput
from .models import Room, Reservation
from django.db import models



class RoomFilter(BaseFilterSet):
    sort_choices = (
        ('asc', 'Возрастанию цены'), ('desc', 'Убыванию цены'), ('number', 'По номеру комнаты')
    )

    check_in = django_filters.DateFilter(widget=DateInput(attrs={'min': date.today()}), label='Заезд')
    check_out = django_filters.DateFilter(widget=DateInput(attrs={'min': date.today()}), label='Выезд')
    person = django_filters.NumberFilter(label='Гости')
    sort_by = django_filters.ChoiceFilter(choices=sort_choices, label='Сортировать по')
    check = django_filters.DateRangeFilter()

    class Meta:
        model = Room
        fields = ['price', ]

    def filter_queryset(self, queryset):
        if self.form.is_valid():
            queryset = super().filter_queryset(queryset)
            cleaned_data = self.form.cleaned_data
            print(cleaned_data)
            print(queryset)

        # if check_in and check_out:
        #     # return Reservation.check_booking(check_in,check_out,p)
        return queryset



