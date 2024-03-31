from django.urls import path
from .views import RoomViewSet, ReservationViewSet, NotBookedRoomViewSet, ReservationView, Home

urlpatterns = [
    path('api/rooms/all', RoomViewSet.as_view({'get': 'list'})),
    path('api/reservations/all', ReservationViewSet.as_view({'get': 'list'})),
    path('api/rooms/available', NotBookedRoomViewSet.as_view({'get': 'list'})),
    path('', Home.as_view(), name='index'),
    path('room/<int:pk>', ReservationView.as_view(), name='reservation')
]