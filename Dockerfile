FROM python:3.10-slim-buster

WORKDIR /usr/src/booking_hotel

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get install -y gcc

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/requirements.txt

RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/booking_hotel

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]