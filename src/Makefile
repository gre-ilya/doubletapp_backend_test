all: migrate runserver

migrate:
	python manage.py migrate $(if $m, api $m,)

createsuperuser:
	python manage.py createsuperuser --no-input

collectstatic:
	python manage.py collectstatic --no-input

dev:
	python manage.py runall 0.0.0.0:8000

shell:
	python manage.py shell

runserver:
	python manage.py runserver 0.0.0.0:8000

runbot:
	python manage.py runbot

runall:
	python manage.py runall 

