from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets

from .forms import DateForm, ReservationForm
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from rest_framework.exceptions import ValidationError
from datetime import datetime as dt
from .utils import sort_rooms
from .permissions import UserPermission


class Home(FormMixin, ListView):
    template_name = 'index.html'
    form_class = DateForm
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = None  # возвращаем queryset
        form = DateForm(self.request.GET)
        if form.is_valid():
            check_in = form.cleaned_data.get('check_in')  # Получение данных из формы
            check_out = form.cleaned_data.get('check_out')
            print(self.request.session['check_in'])
            if str(check_in) > str(check_out):
                raise ValidationError("Неверно указаны даты")
            if (check_in and not check_out) or (check_out and not check_in):
                raise ValidationError('Вторая дата не введена')

            guests = form.cleaned_data.get('guests')
            sort_by = form.cleaned_data.get('sort')
            queryset = sort_rooms(sort_by, check_in, check_out, guests)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_data = {'check_in': self.request.GET.get('check_in', None),
                        'check_out': self.request.GET.get('check_out', None),
                        'guests': self.request.GET.get('guests', None),
                        'sort': self.request.GET.get('sort', None)}
        self.request.session['check_in'] = self.request.GET.get('check_in', None)
        self.request.session['check_out'] = self.request.GET.get('check_out', None)
        self.request.session.modified = True
        form = DateForm(initial=initial_data)
        context['form'] = form
        return context


class ReservationView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = ReservationForm
    template_name = 'reservation.html'
    success_url = reverse_lazy('index')
    login_url = "/account/login/"
    redirect_field_name = ''

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['initial'] = {
            'check_in': self.request.session.get('check_in'),
            'check_out': self.request.session.get('check_out')
        }
        print(kwargs)
        return kwargs


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('number')
    serializer_class = RoomSerializer
    permission_classes = [UserPermission]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [UserPermission]


class NotBookedRoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [UserPermission]

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
