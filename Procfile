web: gunicorn SMSReminder.wsgi
celery: python manage.py celery worker -A SMSReminder -B --concurrency=1