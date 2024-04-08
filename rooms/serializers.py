from rest_framework import serializers

from .models import Room, Reservation


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        read_only_fields = ('active',)
        fields = ('room', 'check_in', 'check_out', 'active',)


class ReservationSerializerUpdateStatusActive(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        read_only_fields = ('room', 'check_in', 'check_out',)
        fields = ('room', 'check_in', 'check_out', 'active')
