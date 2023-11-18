# syntax=docker/dockerfile:1

################################
# PYTHON-BASE
################################
FROM python:3.8.5-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    VIRTUAL_ENV="/venv"

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

# Prepare virtual environment
RUN python -m venv $VIRTUAL_ENV

# Set working directory
WORKDIR /app
ENV PYTHONPATH="/app:$PYTHONPATH"

################################
# BUILDER-BASE
################################
FROM python-base as builder-base
RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    gnupg \
    ca-certificates \
    build-essential \
    git \
    nano \
    curl

# Poetry and Pip store their cache so that they can re-use it
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

# ADD Your Code Here
WORKDIR /app
COPY poetry.lock pyproject.toml ./
COPY statefarm/ ./statefarm/

# install runtime deps to VIRTUAL_ENV
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --no-dev

################################
# PRODUCTION
################################
FROM python-base as production

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates && \
    apt-get clean

# Copy the virtual environment with dependencies from the builder base
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

# Copy application code and model file
WORKDIR /app
COPY poetry.lock pyproject.toml ./
COPY statefarm/ ./statefarm
WORKDIR /app/statefarm

# Expose the port FastAPI will run on
EXPOSE 8080

# Run FastAPI server
CMD ["uvicorn", "statefarm.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
