from django.urls import path, include
from .views import RoomViewSet, ReservationViewSet, NotBookedRoomViewSet, ReservationView, Home
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/reservations/', ReservationViewSet.as_view({'get': 'list'})),
    path('api/reservations/<int:pk>', ReservationViewSet.as_view({'put': 'update'})),
    path('api/rooms/available', NotBookedRoomViewSet.as_view({'get': 'list'})),
    path('', Home.as_view(), name='index'),
    path('room/<int:pk>', ReservationView.as_view(), name='reservation')
]