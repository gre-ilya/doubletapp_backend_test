all: build run

all-d: build run-d

build:
	docker compose build

run:
	docker compose up

run-d:
	docker compose up -d

migrate:
	python src/manage.py migrate $(if $m, api $m,)

makemigrations:
	python src/manage.py makemigrations
	sudo chown -R ${USER} app/migrations/

createsuperuser:
	python src/manage.py createsuperuser --no-input

collectstatic:
	python src/manage.py collectstatic --no-input

dev:
	python src/manage.py runall 0.0.0.0:8000

command:
	python src/manage.py ${c}

shell:
	python src/manage.py shell

runserver:
	python src/manage.py runserver

runbot:
	python src/manage.py runbot

runall:
	python src/manage.py runall 

debug:
	python src/manage.py debug

piplock:
	pipenv install
	sudo chown -R ${USER} Pipfile.lock

lint:
	isort .
	flake8 --config setup.cfg
	black --config pyproject.toml .

check_lint:
	isort --check --diff .
	flake8 --config setup.cfg
	black --check --config pyproject.toml .
