from celery import Celery

from domain.usecases.transcriptome.input.conversion_sra_to_fasta_usecase_input import (
    ConversionSraToFastaUseCaseInput,
)
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)

app = Celery(
    "geo",
    broker="pyamqp://admin:pass@rabbitmq:5672//",
    include=[
        # 'tasks.geo_task'
        "infrastructure.messaging.task"
    ],
)


def convert_sra_to_fasta_task(sra_id, pipeline_id, organism_group):
    app.send_task(
        "infrastructure.messaging.task.sra_to_fasta_conversion",
        args=(sra_id, pipeline_id, organism_group),
        queue="sra_to_fasta_conversion",
    )


def download_sra_task(sra_id, pipeline_id, organism_group):
    app.send_task(
        "infrastructure.messaging.task.sra_transcriptome_download",
        args=(sra_id, pipeline_id, organism_group),
        queue="geo_sra_download",
    )
