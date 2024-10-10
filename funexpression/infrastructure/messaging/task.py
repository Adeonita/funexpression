from domain.usecases.base_usecase import BaseUseCase
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)
from infrastructure.celery import app
from ports.infrastructure.messaging.task_port import TaskPort


class Task(TaskPort):

    def __init__(self, use_case: BaseUseCase):
        self.base_usecase = use_case

    @app.task(queue="geo_sra_download")
    def sra_transcriptome_download(self, sra_id: str, pipeline_id: int):
        try:
            input = TranscriptomeDownloadUseCaseInput(
                sra_id=sra_id, pipeline_id=pipeline_id
            )
            self.base_usecase.execute(input)
        except Exception as e:
            return f"there was an error when downloading sra sequence {e}"

    @app.task(queue="sra_to_fasta_conversion")
    def sra_to_fasta_conversion(self, pipeline_id: str):
        try:
            self.base_usecase.execute(pipeline_id)
        except Exception as e:
            return f"there was an error when downloading sra sequence {e}"
