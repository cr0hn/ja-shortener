FROM python:3.11-alpine AS base

RUN addgroup -S ja_shortener && \
    adduser -S -G ja_shortener -s /bin/false ja_shortener && \
    apk update && apk upgrade && apk add --no-cache curl && \
    mkdir /staticfiles /data

FROM base AS builder

ENV POETRY_VIRTUALENVS_CREATE=false
ENV POSTGRES_CLIENT_VERSION=postgresql15-client-15.13-r0

RUN apk add build-base libffi-dev openssl-dev ${POSTGRES_CLIENT_VERSION} && \
    pip install --disable-pip-version-check --no-cache-dir -U poetry poetry-plugin-export && \
    mkdir /wheels

# Install Web dependencies
COPY ./pyproject.toml ./poetry.lock /dependencies/
RUN cd /dependencies && \
    poetry export -f requirements.txt --output /requirements.txt --without-hashes && \
    pip wheel --no-cache-dir --no-deps --wheel-dir=/wheels -r /requirements.txt

FROM base AS web

COPY --from=builder /wheels /wheels

RUN pip install --disable-pip-version-check --no-cache-dir /wheels/* && \
    rm -rf /wheels

COPY ./deployment/gunicorn.conf.py /gunicorn.conf.py
COPY ./entrypoint-web.sh /entrypoint-web
RUN chmod +x /entrypoint*

COPY ./ja_shortener /ja_shortener
RUN chown -R ja_shortener:ja_shortener /ja_shortener /staticfiles /data

USER ja_shortener
WORKDIR /ja_shortener
RUN python manage.py collectstatic --noinput
ENTRYPOINT ["/entrypoint-web"]