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


# the image is used to run worker for downloading sra files
FROM python:3.11-slim-buster AS download_worker

ENV VIRTUAL_ENV=/app/.venv \
    SRATOOLKIT=/app/sratoolkit \
    PATH="/app/.venv/bin:/app/sratoolkit/bin:$PATH"

WORKDIR /funexpression

COPY --from=builder ${SRATOOLKIT} ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ARG DOWNLOAD_WORKER_CONCURRENCY 
ENV CONCURRENCY=$DOWNLOAD_WORKER_CONCURRENCY

ENTRYPOINT celery -A infrastructure.messaging.task worker -l info --pool=threads --queues=geo_sra_download --concurrency=$CONCURRENCY

# the image is used to run worker for conversion sra to fasta files
FROM python:3.11-slim-buster AS conversion_worker

ENV VIRTUAL_ENV=/app/.venv \
    SRATOOLKIT=/app/sratoolkit \
    PATH="/app/.venv/bin:/app/sratoolkit/bin:$PATH"

WORKDIR /funexpression

COPY --from=builder ${SRATOOLKIT} ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENTRYPOINT ["celery", "-A", "infrastructure.messaging.task", "worker", "-l", "info", "--pool=threads", "--queues=sra_to_fasta_conversion", "--concurrency=3"]

#the image is used to run worker for trimming fasta files
FROM python:3.11-slim-buster AS trimming_worker

RUN apt-get update
RUN apt-get install -y wget unzip
RUN apt-get install -y openjdk-11-jre-headless

RUN wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
RUN unzip Trimmomatic-0.39.zip
RUN mv Trimmomatic-0.39 trimmomatic

ENV VIRTUAL_ENV=/app/.venv \
    JAVA_HOME=/usr/lib/jvm/openjdk-11-jre-headless/jre/bin/java \
    PATH="/app/.venv/bin:/app/java/bin:$PATH"

WORKDIR /funexpression

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENTRYPOINT ["celery", "-A", "infrastructure.messaging.task", "worker", "-l", "info", "--pool=threads", "--queues=trimming_transcriptome", "--concurrency=3"]


# the image is used to run worker for downloading genome files
FROM python:3.11-slim-buster AS genome_download_worker

RUN apt-get -y update
RUN apt-get install -y wget unzip

RUN wget https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/datasets
RUN mv datasets /usr/local/bin
RUN chmod +x /usr/local/bin/datasets


ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/app:$PATH"

WORKDIR /funexpression

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENTRYPOINT ["celery", "-A", "infrastructure.messaging.task", "worker", "-l", "info", "--pool=threads", "--queues=genbank_ncbi_download", "--concurrency=3"]

# the image is used to run worker for aligner transcriptomes
FROM python:3.11-slim-buster as aligner_worker

# dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    vim-common \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# STAR 2.7.11b
RUN wget https://github.com/alexdobin/STAR/archive/refs/tags/2.7.11b.tar.gz \
    && tar -xvzf 2.7.11b.tar.gz \
    && cd STAR-2.7.11b/source \
    && make Depend.list \
    && make STAR \
    && mv STAR /usr/local/bin/ \
    && cd ../../ \
    && rm -rf 2.7.11b.tar.gz STAR-2.7.11b

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/app:$PATH"

WORKDIR /funexpression

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENTRYPOINT ["celery", "-A", "infrastructure.messaging.task", "worker", "-l", "info", "--pool=threads", "--queues=aligner_transcriptome", "--concurrency=2"]

# the image is used to run worker for count transcriptomes
FROM python:3.11-slim-buster as counter_worker

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/app:$PATH"

WORKDIR /funexpression

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}


ENTRYPOINT ["celery", "-A", "infrastructure.messaging.task", "worker", "-l", "info", "--pool=threads", "--queues=counter_transcriptome", "--concurrency=3"]



# the image is used to run worker for aligner transcriptomes
FROM python:3.11-slim-buster as generate_index_genome_worker

# dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    vim-common \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# STAR 2.7.11b
RUN wget https://github.com/alexdobin/STAR/archive/refs/tags/2.7.11b.tar.gz \
    && tar -xvzf 2.7.11b.tar.gz \
    && cd STAR-2.7.11b/source \
    && make Depend.list \
    && make STAR \
    && mv STAR /usr/local/bin/ \
    && cd ../../ \
    && rm -rf 2.7.11b.tar.gz STAR-2.7.11b

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/app:$PATH"

WORKDIR /funexpression

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENTRYPOINT ["celery", "-A", "infrastructure.messaging.task", "worker", "-l", "info", "--pool=threads", "--queues=generate_index_genome", "--concurrency=3"]

FROM python:3.11-slim-buster as differ_worker

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/app:${PATH}"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /funexpression

ENTRYPOINT ["celery", "-A", "infrastructure.messaging.task", "worker", "-l", "info", "--pool=threads", "--queues=generate_diferential_expression", "--concurrency=3"]
