from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormMixin, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from .forms import DateForm, ReservationForm
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from rest_framework.exceptions import ValidationError
from .permissions import ReadPermission
from rest_framework import status
from rest_framework.response import Response


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
            guests = form.cleaned_data.get('guests')
            sort_by = form.cleaned_data.get('sort')
            queryset = Reservation.check_booking(check_in, check_out, guests).order_by(sort_by)
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['initial'] = {
            'room': self.kwargs['pk'],
            'check_in': self.request.session.get('check_in'),
            'check_out': self.request.session.get('check_out')
        }

        return kwargs


class ReservationDeleteView(DeleteView):
    template_name = 'delete_reservation.html'
    success_url = reverse_lazy('reserved')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Reservation.objects.filter(guest=self.request.user.id), pk=pk)


class Profile(ListView):
    template_name = 'profile.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        queryset = Reservation.objects.filter(guest=self.request.user.id)
        return queryset


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('number')
    serializer_class = RoomSerializer
    permission_classes = [ReadPermission]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]


class NotBookedRoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoomSerializer
        elif self.request.method == 'POST':
            return ReservationSerializer

    def get_queryset(self):
        check_in = self.request.query_params.get('check_in')
        check_out = self.request.query_params.get('check_out')
        guests = self.request.query_params.get('guests')
        if not all([check_in, check_out, guests]):
            raise ValidationError("Введите параметры check_in, check_out и guests")
        queryset = Reservation.check_booking(check_in, check_out, guests)
        if not queryset:
            raise ValidationError('Неверно указаны даты')
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        check_in = request.data['check_in']
        check_out = request.data['check_out']
        room = request.data['room']
        if Reservation.check_booking(check_in, check_out, pk=room):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"errors": {
                "body": [
                    "Неправильно указаны даты"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)
