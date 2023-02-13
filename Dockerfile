FROM python:3.9.6-alpine

WORKDIR /home/user/web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunciron

COPY . .

ENTRYPOINT [ "/home/user/web/entrypoint.sh" ]