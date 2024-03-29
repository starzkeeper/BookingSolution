from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import viewsets

from .forms import DateForm
from .models import Room, Reservation
from .serializers import RoomSerializer


def index(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['cin']  # Получение данных из формы
            check_out = form.cleaned_data['cout']
            person = form.cleaned_data['person']
            room = Reservation.check_booking(check_in, check_out, person)
            data = {'rooms': room, 'form': form}
            response = render(request, 'index.html', data)
    else:
        form = DateForm()
        data = {'rooms': rooms, 'form': form}
        response = render(request, 'index.html', data)
    return HttpResponse(response)


class RoomAllAPI(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
