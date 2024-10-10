from domain.factories.conversion.conversion_usecase_factory import (
    ConversionUseCaseFactory,
)

from domain.factories.transcriptome.transcriptome_download_usecase_factory import (
    TranscriptomeDownloadUseCaseFactory,
)
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)
from infrastructure.celery import app
from ports.infrastructure.messaging.task_port import TaskPort


class Task(TaskPort):

    @app.task(queue="geo_sra_download")
    def sra_transcriptome_download(sra_id: str, pipeline_id: int):
        try:
            transcriptome_download_usecase = (
                TranscriptomeDownloadUseCaseFactory.create()
            )
            input = TranscriptomeDownloadUseCaseInput(
                sra_id=sra_id, pipeline_id=pipeline_id
            )
            transcriptome_download_usecase.execute(input)
        except Exception as e:
            return f"there was an error when downloading sra sequence {e}"

    @app.task(queue="sra_to_fasta_conversion")
    def sra_to_fasta_conversion(pipeline_id: str):
        try:
            conversion_sra_to_fasta_usecase = ConversionUseCaseFactory.create()
            conversion_sra_to_fasta_usecase.execute(pipeline_id)
        except Exception as e:
            return f"there was an error when downloading sra sequence {e}"
