FROM python:3.10.10-slim

WORKDIR /home/appuser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN useradd --create-home appuser
USER appuser
COPY . .
