# global variables
ARG PYTHON_TAG=3.11-slim
ARG POETRY_VERSION=1.6.1

# ======================================================================================================================
# poetry image, used to build the virtual environment (without dev dependencies)
# ======================================================================================================================
FROM python:${PYTHON_TAG} AS poetry

WORKDIR /venv

ARG POETRY_VERSION
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# install poetry and begin python environment install
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}
COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# ======================================================================================================================
# runtime image, used to build the system dependencies and python environment (from builder)
# ======================================================================================================================
FROM python:${PYTHON_TAG} AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/venv/.venv \
    PATH="/venv/.venv/bin:$PATH"

# see DL3009 and DL3015 for some specifics around the apt-get commands and flags
RUN apt-get update && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# copy virtual environment, static directory, and cyclops codebase
COPY --from=poetry ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# create folders needed for leveldb and fst data
RUN mkdir /leveldb /fst

# ======================================================================================================================
# application image - no dev dependencies
# ======================================================================================================================
FROM runtime AS application

WORKDIR /app

# copy the codebase
COPY ./myapp ./myapp

# run the uvicorn server
CMD ["uvicorn", "myapp.main:app", "--host", "0.0.0.0", "--port", "80"]

# ======================================================================================================================
# development image - includes extra dev dependencies
# ======================================================================================================================
# FROM runtime AS development
#
# WORKDIR /app
#
# ARG POETRY_VERSION
# ENV POETRY_CACHE_DIR=/tmp/poetry_cache \
#     PATH=/root/.local/bin:$PATH
#
# # install git, poetry (via pipx), and hadolint (via wget, used for linting)
# RUN apt-get update && apt-get -y upgrade \
#     && apt-get install -y --no-install-recommends git=1:2.39.2-1.1 pipx=1.1.0-1 wget=1.21.3-1+b2 \
#     && apt-get clean && rm -rf /var/lib/apt/lists/* \
#     && pipx install poetry==${POETRY_VERSION} \
#     && wget -q -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64 \
#     && chmod +x /bin/hadolint
#
# # install the dev dependencies and ner model (main dependencies already in runtime)
# COPY pyproject.toml poetry.lock ./
# RUN poetry install && rm -rf $POETRY_CACHE_DIR \
#     && python -m spacy download en_core_web_${NER_MODEL_SIZE}
#
# # install pre-commit
# COPY .pre-commit-config.yaml ./
# RUN git init -q && pre-commit install --install-hooks
#
# # install the codebase as a proper package
# COPY README.md ./
# COPY ./cyclops ./cyclops
# COPY ./tests ./tests
# RUN poetry install --only-root
#
# # run the uvicorn server
# CMD ["uvicorn", "cyclops.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
#
