from django.conf import settings
from django.db import models
from django.urls import reverse


class Room(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True, verbose_name='Номер')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    places = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Комнаты'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f'Номер: {self.number}'

    def get_absolute_url(self):
        return reverse('reservation', kwargs={"pk": self.pk})


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return self.guest.username

    @classmethod
    def check_booking(cls, check_in, check_out, person):
        rr = []
        # Фильтрация дат
        for each_reservation in cls.objects.all():
            if str(check_in) < str(each_reservation.check_in) and str(check_out) <= str(each_reservation.check_in):
                pass
            elif str(check_in) >= str(each_reservation.check_out) and str(check_out) > str(
                    each_reservation.check_out):
                pass
            else:
                rr.append(each_reservation.room.number)
        return Room.objects.all().filter(places__gte=person).exclude(number__in=rr)
