from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin, ModelFormMixin
from rest_framework import viewsets

from .forms import DateForm, ReservationForm
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from rest_framework.exceptions import ValidationError
from datetime import datetime as dt
from .utils import sort_rooms


class Home(FormMixin, ListView):
    template_name = 'index.html'
    form_class = DateForm
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = Room.objects.all()  # возвращаем queryset
        form = DateForm(self.request.GET)
        if form.is_valid():
            check_in = form.cleaned_data.get('check_in')  # Получение данных из формы
            check_out = form.cleaned_data.get('check_out')
            if str(check_in) > str(check_out):
                return HttpResponse('Неверно указаны даты')

            guests = form.cleaned_data.get('guests')
            sort_by = form.cleaned_data.get('sort')
            queryset = sort_rooms(sort_by, check_in, check_out, guests)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context


class ReservationView(ModelFormMixin, DetailView):
    model = Room
    form_class = ReservationForm
    template_name = 'reservation.html'
    success_url = reverse_lazy('index')


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('number')
    serializer_class = RoomSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class NotBookedRoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer

    def get_queryset(self):
        check_in = self.request.query_params.get('check_in')  # Получение данных из формы
        check_out = self.request.query_params.get('check_out')
        guests = self.request.query_params.get('guests')
        if not all([check_in, check_out, guests]):
            raise ValidationError("Введите параметры check_in, check_out и person")
        if check_in > check_out:
            raise ValidationError('Неверно указана дата въезда')
        try:
            dt.strptime(check_in, '%Y-%m-%d')
            dt.strptime(check_out, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Неверно указаны даты')
        queryset = Reservation.check_booking(check_in, check_out, guests)
        return queryset
