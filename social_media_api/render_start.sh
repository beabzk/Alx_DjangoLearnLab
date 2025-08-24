#!/usr/bin/env bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --no-input

exec gunicorn social_media_api.wsgi:application --log-file -
