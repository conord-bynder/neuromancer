FROM 893087526002.dkr.ecr.eu-west-1.amazonaws.com/bynder-python:3.7-slim as base

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv sync

# The `test-base` stage is used as the base for images that require
# the development dependencies. The duplication of the COPY instruction
# avoids breaking the cache for that later when the Pipfile changes
FROM base AS Unittest

# Install Python dependencies
RUN pipenv sync --dev

COPY tests tests
COPY neuromancer neuromancer

# The `Production` stage is the default stage if the Dockerfile is run without
# a target stage set.
FROM base As Production

COPY newrelic.ini .
COPY setup.py .
COPY ./config.*.ini /app/
COPY ./VERSION /app/
COPY neuromancer neuromancer

RUN pipenv run pip install -e .
EXPOSE 8080

ENV NEW_RELIC_CONFIG_FILE newrelic.ini

# Gunicorn for Docker settings / https://pythonspeed.com/articles/gunicorn-in-docker/
CMD [ \
    "pipenv", "run", \
    "newrelic-admin", "run-program", \
    "gunicorn", "neuromancer.app:run_app", \
    "--bind", "0.0.0.0:8080", \
    "--worker-class", "aiohttp.worker.GunicornWebWorker", \
    "--worker-tmp-dir", "/dev/shm", \
    "--threads", "4" \
]
