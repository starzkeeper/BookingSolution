from django.urls import path
from .views import ReservationListCreateAPIView, ReservationRetrieveUpdateAPIView, RoomListAPIView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('api/rooms/', RoomListAPIView.as_view(), name='rooms'),
    path('api/reservations/', ReservationListCreateAPIView.as_view(), name='booking-create'),
    path('api/reservations/', ReservationListCreateAPIView.as_view(), name='booking-my'),
    path('api/reservations/<int:pk>', ReservationRetrieveUpdateAPIView.as_view(), name='booking-detail'),
    path('api/reservations/<int:pk>', ReservationRetrieveUpdateAPIView.as_view(), name='booking-update'),
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
