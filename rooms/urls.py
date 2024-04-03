from django.urls import path, include
from .views import RoomViewSet, ReservationViewSet, ReservationView, Home, Profile, ReservationDeleteView, NotBookedRoomViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

router = routers.SimpleRouter()
router.register(r'rooms', RoomViewSet)
router.register('reservations', ReservationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(router.urls)),
    path('api/rooms/available', NotBookedRoomViewSet.as_view({'get': 'list'})),
    path('api/rooms/available/room-reservation', NotBookedRoomViewSet.as_view({'post': 'create'})),
    path('', Home.as_view(), name='index'),
    path('room/<int:pk>', ReservationView.as_view(), name='reservation'),
    path('reserved/', Profile.as_view(), name='reserved'),
    path('reserved/<int:pk>', ReservationDeleteView.as_view(), name='delete-reservation'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]