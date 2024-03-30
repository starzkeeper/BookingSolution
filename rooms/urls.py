from django.contrib import admin
from django.urls import path, include
from .views import RoomViewSet, index, ReservationViewSet, NotBookedRoomViewSet

urlpatterns = [
    path('api/rooms/all', RoomViewSet.as_view({'get': 'list'})),
    path('api/reservations/all', ReservationViewSet.as_view({'get': 'list'})),
    path('api/rooms/available', NotBookedRoomViewSet.as_view({'get': 'list'})),
    path('', index, name='index')
]