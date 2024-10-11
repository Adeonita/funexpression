from domain.factories.transcriptome.conversion_sra_to_fasta_usecase_factory import (
    ConversionSraToFastaUseCaseFactory,
)
from domain.factories.transcriptome.transcriptome_download_usecase_factory import (
    TranscriptomeDownloadUseCaseFactory,
)
from domain.usecases.base_usecase import BaseUseCase
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)
from infrastructure.celery import app
from ports.infrastructure.messaging.task_port import TaskPort


class Task(TaskPort):

    @app.task(bind=True, queue="geo_sra_download")
    def sra_transcriptome_download(self, sra_id: str, pipeline_id: str):

        print(f"Aqui é o sra_id: {sra_id}")
        print(f"Aqui é o pipeline_id: {pipeline_id}")
        # TODO: testar o fluxo completo englobando a realizacao do download novamente (remover o download existente)
        # try:
        #     transcriptome_download_usecase = (
        #         TranscriptomeDownloadUseCaseFactory.create()
        #     )

        #     input = TranscriptomeDownloadUseCaseInput(
        #         sra_id=sra_id, pipeline_id=pipeline_id
        #     )
        #     transcriptome_download_usecase.execute(input)
        # except Exception as e:
        #     return f"there was an error when downloading sra sequence {e}"

    @app.task(queue="sra_to_fasta_conversion")
    def sra_to_fasta_conversion(self, pipeline_id: str):
        try:
            conversion_usecase = ConversionSraToFastaUseCaseFactory.create()
            conversion_usecase.execute("67071045fa9904a7632389be")
        except Exception as e:
            return f"there was an error when downloading sra sequence {e}"


# celery -A infrastructure.messaging.task worker -l info --pool=threads --queues=geo_sra_download
