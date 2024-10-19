from domain.entities.triplicate import OrganinsGroupEnum
from domain.factories.transcriptome.conversion_sra_to_fasta_usecase_factory import (
    ConversionSraToFastaUseCaseFactory,
)
from domain.factories.transcriptome.transcriptome_download_usecase_factory import (
    TranscriptomeDownloadUseCaseFactory,
)
from domain.factories.transcriptome.transcriptome_trimming_usecase_factory import (
    TranscriptomeTrimmingUseCaseFactory,
)
from domain.usecases.base_usecase import BaseUseCase
from domain.usecases.transcriptome.input.conversion_sra_to_fasta_usecase_input import (
    ConversionSraToFastaUseCaseInput,
)
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)
from domain.usecases.transcriptome.input.trimming_transcriptome_usecase_input import (
    TrimmingTranscriptomeUseCaseInput,
    TrimmingTypeEnum,
)
from infrastructure.celery import app
from ports.infrastructure.messaging.task_port import TaskPort


class Task(TaskPort):

    @app.task(bind=True, queue="geo_sra_download")
    def sra_transcriptome_download(
        self, sra_id: str, pipeline_id: str, organism_group: str
    ):

        print(f"Aqui é o sra_id: {sra_id}")
        print(f"Aqui é o pipeline_id: {pipeline_id}")
        # TODO: testar o fluxo completo englobando a realizacao do download novamente (remover o download existente)
        # try:
        #     transcriptome_download_usecase = (
        #         TranscriptomeDownloadUseCaseFactory.create()
        #     )

        #     input = TranscriptomeDownloadUseCaseInput(
        #         sra_id=sra_id, pipeline_id=pipeline_id, organism_group=organism_group
        #     )
        #     transcriptome_download_usecase.execute(input)
        # except Exception as e:
        #     return f"there was an error when downloading sra sequence {e}"

    @app.task(bind=True, queue="sra_to_fasta_conversion")
    def sra_to_fasta_conversion(self, sra_id, pipeline_id, organism_group):
        try:
            conversion_usecase = ConversionSraToFastaUseCaseFactory.create()
            conversion_usecase.execute(sra_id, pipeline_id, organism_group)
        except Exception as e:
            return f"there was an error when downloading sra sequence {e}"

    @app.task(bind=True, queue="trimming_transcriptome")
    def trimming_transcriptome(
        self,
        pipeline_id: str,
        sra_id: str,
        organism_group: str,
        trimming_type: TrimmingTypeEnum,
        input_path: str,
        output_path: str,
    ):
        try:
            input = TrimmingTranscriptomeUseCaseInput(
                pipeline_id=pipeline_id,
                sra_id=sra_id,
                organism_group=organism_group,
                trimming_type=trimming_type,
                input_path=input_path,
                output_path=output_path,
            )
            trimming_usecase = TranscriptomeTrimmingUseCaseFactory.create()
            trimming_usecase.execute(input)
        except Exception as e:
            return f"there was an error when trimming the transcriptome {e}"
