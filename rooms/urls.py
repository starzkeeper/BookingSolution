from django.contrib import admin
from django.urls import path, include
from .views import RoomAllAPI, index

urlpatterns = [
    path('api/rooms/all', RoomAllAPI.as_view({'get': 'list'})),
    path('', index, name='index')
]