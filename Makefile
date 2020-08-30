.PHONY: init run db

init:
	python manage.py db init && python manage.py init

db:
	python manage.py create-db && python manage.py init

run:
	python manage.py run