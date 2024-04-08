from datetime import date, datetime, timedelta

import django_filters
from rest_framework.exceptions import ValidationError

from .models import Reservation
from rooms.models import Room


class RoomFilter(django_filters.FilterSet):
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    places_gte = django_filters.NumberFilter(field_name='places', lookup_expr='gte')
    places_lte = django_filters.NumberFilter(field_name='places', lookup_expr='lte')

    check_in = django_filters.DateFilter(method='get_available_rooms', field_name='available_rooms', label='Check in')
    check_out = django_filters.DateFilter(method='get_available_rooms', field_name='available_rooms', label='Check out')

    def get_available_rooms(self, qs, *args):
        check_in = self.request.query_params.get('check_in', date.today())
        if isinstance(check_in, str):
            check_in = datetime.strptime(check_in, '%Y-%m-%d').date()

        check_out = self.request.query_params.get('checkout', check_in + timedelta(days=1))
        if isinstance(check_out, str):
            check_out = datetime.strptime(check_out, '%Y-%m-%d').date()

        if check_in == check_out:
            raise ValidationError('Дата check_out не может быть равна дате check_in')
        elif check_in > check_out:
            raise ValidationError('Дата заезда не может быть меньше даты выезда')

        reserved_rooms_ids = Reservation.objects.get_intersections(check_in, check_out).values('room')
        if reserved_rooms_ids:
            qs = qs.exclude(number__in=reserved_rooms_ids)
        return qs

    order_by = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('places', 'places'),
        ),
        field_labels={
            'price': 'Цена',
            'places': 'Количество мест',
        }
    )

    class Meta:
        model = Room
        fields = ['price_gte', 'price_lte', 'places_gte', 'places_lte']
