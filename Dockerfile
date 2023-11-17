# syntax=docker/dockerfile:1

################################
# PYTHON-BASE
################################
FROM python:3.7.17-slim as python-base

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

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Copy project files (Poetry lock file and pyproject.toml)
COPY poetry.lock pyproject.toml ./

# Install dependencies in the virtual environment
RUN poetry install --no-root --no-dev

################################
# PRODUCTION
################################
FROM python-base as production

# Copy the virtual environment with dependencies from the builder base
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

# Copy application code and model file
WORKDIR /app
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8080

# Run FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
