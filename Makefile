.PHONY: run migrate makemigrations shell test lint

run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

shell:
	python manage.py shell

test:
	pytest

lint:
	ruff check .
