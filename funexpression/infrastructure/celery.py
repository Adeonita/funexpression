from celery import Celery

from domain.usecases.conversion.input.conversion_sra_to_fasta_usecase_input import (
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


def convert_sra_to_fasta_task(input: ConversionSraToFastaUseCaseInput):
    app.send_task(
        "infrastructure.messaging.task.sra_to_fasta_conversion",
        args=(input.sra_id, input.pipeline_id, input.organism_group),
        queue="sra_to_fasta_conversion",
    )


def download_sra_task(input: TranscriptomeDownloadUseCaseInput):
    app.send_task(
        "infrastructure.messaging.task.sra_transcriptome_download",
        args=(input.sra_id, input.pipeline_id),
        queue="geo_sra_download",
    )
