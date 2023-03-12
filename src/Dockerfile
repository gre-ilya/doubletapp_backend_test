FROM python:3.10.10-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN useradd --create-home appuser
USER appuser

WORKDIR /home/appuser
COPY . .
