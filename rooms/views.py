from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from rest_framework import viewsets

from .forms import DateForm, ReservationForm
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from rest_framework.exceptions import ValidationError
from datetime import datetime as dt
from .utils import sort_rooms


def index(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['cin']  # Получение данных из формы
            check_out = form.cleaned_data['cout']
            if str(check_in) > str(check_out):
                return HttpResponse('Неверно указаны даты')

            person = form.cleaned_data['person']
            sort_by = form.cleaned_data['sort']
            rooms = sort_rooms(sort_by, check_in, check_out, person)
            data = {'rooms': rooms, 'form': form}
            response = render(request, 'index.html', data)
    else:
        form = DateForm()
        data = {'form': form}
        response = render(request, 'index.html', data)
    return HttpResponse(response)


class ReservationView(FormMixin, DetailView):
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
        check_in = self.request.query_params.get('cin')  # Получение данных из формы
        check_out = self.request.query_params.get('cout')
        person = self.request.query_params.get('person')
        if not all([check_in, check_out, person]):
            raise ValidationError("Введите параметры cin, cout и person")
        if check_in > check_out:
            raise ValidationError('Неверно указана дата въезда')
        try:
            dt.strptime(check_in, '%Y-%m-%d')
            dt.strptime(check_out, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Неверно указаны даты')
        queryset = Reservation.check_booking(check_in, check_out, person)
        return queryset
