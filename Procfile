web: python manage.py migrate --noinput && gunicorn bibliotheque_project.wsgi:application --bind 0.0.0.0:$PORT --workers=2 --timeout=90
