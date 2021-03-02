FROM 893087526002.dkr.ecr.eu-west-1.amazonaws.com/bynder-python:3.7 as base

USER root
RUN chown bynder /app
USER bynder

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv sync

# The `test-base` stage is used as the base for images that require
# the development dependencies. The duplication of the COPY instruction
# avoids breaking the cache for that later when the Pipfile changes
FROM base AS test-base

USER root
RUN apk add --no-cache --virtual build-dependencies gcc g++ make
USER bynder

# Install Python dependencies
RUN pipenv sync --dev

COPY tests tests
COPY neuromancer neuromancer

# The `Lint` stage runs the application lint checks
FROM test-base AS Lint

COPY pylintrc .
COPY .flake8 .
RUN pipenv run pylint neuromancer tests
RUN pipenv run flake8  .

# The `Mypy` stage runs the application typing checks
FROM test-base AS Mypy

COPY mypy.ini .
RUN pipenv run mypy .

# The `Bandit` stage runs the application security code analysis checks
FROM test-base AS Bandit

RUN pipenv run bandit -r neuromancer 

# The `Unittest` stage runs the application unit tests, the build will fail
# if the tests fail.
FROM test-base AS Unittest

COPY .coveragerc .
RUN pipenv run pytest \
    -v \
    --cov neuromancer \
    --cov-report term-missing \
    --cov-report xml \
    tests

# The `Production` stage is the default stage if the Dockerfile is run without
# a target stage set.
FROM base As Production

USER root
RUN apk del build-dependencies
USER bynder

COPY setup.py .
COPY ./config.*.ini /app/
COPY neuromancer neuromancer

