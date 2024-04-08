from django.conf import settings
from django.db import models
from django.db.models import Q, F, QuerySet
from django.urls import reverse
from datetime import datetime as dt
import datetime
from django.core.exceptions import ValidationError


class Room(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True, verbose_name='Номер')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    places = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Комнаты'
        verbose_name_plural = 'Комнаты'

    def delete(self, using=None, keep_parents=False):
        active_bookings = self.reservations.filter(active=True, checkout__gt=datetime.date.today())
        if active_bookings.exists():
            raise ValidationError('Нельзя удалить комнаты брони которых активны и дата выезда больше текущей!')
        super().delete(using, keep_parents)

    def __str__(self):
        return f'Номер: {self.number}'

    def get_absolute_url(self):
        return reverse('reservation', kwargs={"pk": self.pk})


class ReservationQuerySet(models.QuerySet):

    def get_intersections(
            self,
            check_in: dt.date,
            check_out: dt.date,
            room: Room | None = None
    ) -> QuerySet:
        lookup = ((
                          Q(check_in__lt=check_out) & Q(check_out__gt=check_in)) | (
                          Q(check_in=check_in) & Q(check_out__gt=check_in)) | (
                          Q(check_in__lt=check_out) & Q(check_out=check_out))
                  )
        qs = self
        if room:
            qs = self.filter(room=room)
        qs = qs.filter(lookup)
        return qs


class ReservationManager(models.Manager):

    def get_queryset(self):
        return ReservationQuerySet(self.model, using=self._db)

    def get_intersections(
            self,
            check_in: dt.date,
            check_out: dt.date,
            room: Room | None = None
    ) -> QuerySet:
        active_bookings = self.get_queryset().filter(active=True)
        return active_bookings.get_intersections(check_in, check_out, room)


class Reservation(models.Model):
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    active = models.BooleanField(default=True)

    objects = ReservationManager()

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        constraints = [
            models.CheckConstraint(
                check=Q(check_out__gt=F('check_in')),
                name='check_in_before_check_out'
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.check_in} - {self.check_out}'

    def get_absolute_url(self):
        return reverse('delete-reservation', kwargs={"pk": self.pk})

    def clean(self):
        super().clean()
        existing_bookings = Reservation.objects.get_intersections(
            self.check_in, self.check_out, self.room).exclude(id=self.id)
        if existing_bookings.all():
            raise ValidationError('Выбранная дата уже занята!')

    def save(self, *args, **kwargs):
        if self.active:
            self.clean()
        super().save(*args, **kwargs)
