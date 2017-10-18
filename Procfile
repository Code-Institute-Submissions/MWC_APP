release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn MWC_APP.wsgi --log-file -