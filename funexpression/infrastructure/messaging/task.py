from typing import Callable
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
