FROM python:3.10.10-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update  \
    && apt-get install -y make \
    && apt-get install -y isort \
    && apt-get install -y flake8 \
    && apt-get install -y black

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

RUN useradd --create-home appuser
USER appuser

WORKDIR /home/appuser
COPY . .

ENTRYPOINT ["bash"]
