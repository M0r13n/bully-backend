web: python wsgi.py
# Always run DB migrations

postdeploy: make db && python manage.py db upgrade

