from rest_framework.exceptions import ValidationError

from rooms.models import Reservation


def sort_rooms(sort_by, check_in, check_out, person):
    rooms = None
    if sort_by == 'asc':
        rooms = Reservation.check_booking(check_in, check_out, person).order_by('price')
    elif sort_by == 'desc':
        rooms = Reservation.check_booking(check_in, check_out, person).order_by('-price')
    elif sort_by == 'number':
        rooms = Reservation.check_booking(check_in, check_out, person).order_by('number')
    return rooms
