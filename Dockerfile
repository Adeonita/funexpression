FROM python:3.11-buster AS builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

#install sra toolkit
RUN wget http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.1.1/sratoolkit.3.1.1-ubuntu64.tar.gz
RUN tar -xvf sratoolkit.3.1.1-ubuntu64.tar.gz
RUN mv sratoolkit.3.1.1-ubuntu64 sratoolkit

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/app:${PATH}}"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY funexpression ./funexpression

WORKDIR /funexpression


ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]


# the image is used to run worker
FROM python:3.11-slim-buster AS worker

ENV VIRTUAL_ENV=/app/.venv \
    SRATOOLKIT=/app/sratoolkit \
    PATH="/app/.venv/bin:/app/sratoolkit/bin:$PATH"

WORKDIR /funexpression

COPY --from=builder ${SRATOOLKIT} ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . /funexpression

ENTRYPOINT ["celery", "-A", "tasks.geo_task", "worker", "-l", "info", "--pool=threads"]
