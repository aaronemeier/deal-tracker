ARG PYTHON_VERSION=3.11

FROM python:$PYTHON_VERSION-bookworm AS base

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CHROMEDRIVER_DIR=/chromedriver
WORKDIR /app

RUN apt-get update &&  apt-get install --no-install-recommends -y \
    # This are build dependencies for Psycopg (Postgres Adapter)
    # It is recommended by the Authors to compile from source for production
    gcc python3-dev libpq-dev \
    # For translations
    gettext \
    # For Chrome \
    curl gnupg build-essential apt-transport-https ca-certificates wget unzip gnupg && \
    curl https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    # Set up Chromedriver
    export CHROME_VERSION=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") &&\
    export CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION") &&\
    mkdir $CHROMEDRIVER_DIR &&\
    wget -P $CHROMEDRIVER_DIR "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip" &&\
    unzip $CHROMEDRIVER_DIR/chromedriver* -d /usr/local/bin/ &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install poetry
RUN python -m venv /venv
COPY pyproject.toml poetry.lock ./
RUN poetry export --format requirements.txt --without-hashes --no-interaction | /venv/bin/pip install -r /dev/stdin
COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base AS runtime
ARG SITE_VERSION="dev"
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WEB_CONCURRENCY=3

WORKDIR /app/
COPY --from=builder /venv /venv
COPY . /app/
RUN echo "SITE_VERSION = '${SITE_VERSION}'" > /app/deal_tracker_config/build_config.py

RUN /venv/bin/python manage.py compilemessages
RUN /venv/bin/python manage.py collectstatic --noinput --link

RUN useradd --create-home appuser &&\
     mkdir -p /app/staticfiles &&\
     mkdir -p /app/mediafiles &&\
     chown -R appuser.appuser /app/staticfiles &&\
     chown -R appuser.appuser /app/mediafiles && \
     chown -R appuser.appuser /venv/

USER appuser

ENV PATH="/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", \
   "--log-level=info", \
   "--host=0.0.0.0", \
   "--port=8000", \
   "--proxy-headers", \
   "deal_tracker_config.asgi:application" \
]
