#!/usr/bin/env sh

export GUNICORN_LOG_LEVEL="${LOG_LEVEL:-INFO}"
export GUNICORN_WORKERS="${GUNICORN_WORKERS:-5}"

python manage.py migrate --noinput

if [ -n "$SUPERUSER_USERNAME" ] && [ -n "$SUPERUSER_PASSWORD" ]; then
    python manage.py ja_createsuperuser "$SUPERUSER_USERNAME" "$SUPERUSER_EMAIL" "$SUPERUSER_PASSWORD" || true
fi


exec gunicorn --log-level "${GUNICORN_LOG_LEVEL}" -c /gunicorn.conf.py  --bind ":8080" -w ${GUNICORN_WORKERS} -k gevent --timeout 20 ja_settings.wsgi:application
