FROM python:3.12-slim AS beaver_api

ARG APP_PATH=/opt/app
ARG USER=1000
ARG GROUP=1000

ENV PYTHONUNBUFFERED=1 \
  # Prevents python creating .pyc files
  PYTHONDONTWRITEBYTECODE=1 \
  \
  # Pip
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry
  POETRY_VERSION=1.6.1 \
  # Make poetry install to this location
  POETRY_HOME="/usr/local" \
  # Make poetry not create a virtual environment
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR="/var/cache/pypoetry" \
  # Do not ask any interactive question
  POETRY_NO_INTERACTION=1

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  curl \
  # dependencies for building Python packages
  build-essential \
  # psycopg dependencies
  libpq-dev

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

    RUN groupadd -g ${GROUP} appgroup && \
    useradd -r -u  ${USER} -g appgroup appuser

# Copy app code to WORKDIR
WORKDIR $APP_PATH
COPY --chown=${USER}:${GROUP} . ${APP_PATH}

# Make $USER owner of the WORKDIR directory as well
RUN chown -R ${USER}:${GROUP} ${APP_PATH}

RUN poetry install

USER ${USER}:${GROUP}

