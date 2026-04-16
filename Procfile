web: python manage.py migrate --noinput && python manage.py createsuperuserifnotexists && gunicorn bibliotheque_project.wsgi:application --bind 0.0.0.0:$PORT --workers=2 --timeout=90
