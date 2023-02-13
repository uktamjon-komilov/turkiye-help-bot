FROM python:3.11-alpine

WORKDIR /home/user/web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn==20.1.0
RUN pip install psycopg2-binary==2.9.5

COPY . .

ENTRYPOINT [ "/home/user/web/entrypoint.sh" ]