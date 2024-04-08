from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .mixins import UserQuerySetMixin
from .models import Room, Reservation
from .pagination import RoomsPagination
from .serializers import RoomSerializer, ReservationSerializer, ReservationSerializerUpdateStatusActive
from rest_framework.exceptions import ValidationError
from rest_framework import status
import django_filters
from .filters import RoomFilter


class RoomListAPIView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = RoomFilter
    pagination_class = RoomsPagination

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except ValidationError as exc:
            return JsonResponse({'detail': '{}'.format(*exc.args)}, status=400)


class ReservationListCreateAPIView(UserQuerySetMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    allow_superuser_view = False

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError:
            return JsonResponse(status=status.HTTP_409_CONFLICT, data={'detail': 'dates are already taken'})

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ReservationRetrieveUpdateAPIView(UserQuerySetMixin, RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializerUpdateStatusActive
    lookup_field = 'pk'
    allow_superuser_view = True
    user_field = 'user'
    queryset = Reservation.objects.all()
    http_method_names = ('patch', 'get',)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
