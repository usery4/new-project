FROM python:3.8.0-alpine
ENV PYTHONUNBUFFERED 1


RUN python -m pip install --upgrade pip
RUN pip install dj-database-url
RUN pip install django
RUN pip install djangorestframework
RUN pip install django-filter
RUN pip install django-admin-interface
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev
RUN pip install psycopg2==2.8.6


WORKDIR /code
COPY . /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt



