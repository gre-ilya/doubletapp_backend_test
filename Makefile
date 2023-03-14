IMAGE_NAME=${CI_REGISTRY}/ilya.grubenuk/ci-cd/ci-cd:${CI_ENVIRONMENT_SLUG}-${CI_COMMIT_SHA}

all: migrate runserver

build:
	docker build -t ${IMAGE_NAME} ./src

push:
	docker push ${IMAGE_NAME}

pull:
	docker pull ${IMAGE_NAME}

up:
	docker-compose up -d

down:
	docker-compose down

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
	python src/manage.py runserver 0.0.0.0:8000

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
	isort --check --diff -rc .
	flake8 --config setup.cfg
#	black --check --config pyproject.toml .
