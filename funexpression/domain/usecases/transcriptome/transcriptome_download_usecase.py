from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum

# from domain.factories.transcriptome.conversion_sra_to_fasta_usecase import (
#     ConversionSraToFastaUseCaseFactory,
# )
from domain.usecases.base_usecase import BaseUseCase
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)
from ports.infrastructure.bio_database.geo_adapter_port import GeoAdapterPort

# from ports.infrastructure.messaging.task_port import TaskPort
from ports.infrastructure.messaging.task_port import TaskPort
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)


class TranscriptomeDownloadUseCase(BaseUseCase):

    def __init__(
        self,
        geo_adapter: GeoAdapterPort,
        pipeline_repository: PipelineRepositoryPort,
        task: TaskPort,
    ):
        self.geo_adapter = geo_adapter
        self.pipeline_repository = pipeline_repository
        self.task = task
        # self.conversion_sra_to_fasta_usecase = (
        #     ConversionSraToFastaUseCaseFactory.create()
        # )

    def execute(self, input: TranscriptomeDownloadUseCaseInput) -> str:
        print(f"Processing download for {input.sra_id}")
        sra_path = self.geo_adapter.get_sra_sequence_from_ncbi(input.sra_id)
        self.pipeline_repository.update_sra_file_status(
            pipeline_id=input.pipeline_id,
            sra_id=input.sra_id,
            status=SRAFileStatusEnum.OK,
        )

        if self.pipeline_repository.is_all_file_download_completed(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id,
                pipeline_stage=PipelineStageEnum.DOWNLOADED,
            )
            print("Download step done")

            # aqui
            print("Sending to the conversion queue...")
            self.task.convert_sra_to_fasta(pipeline_id=input.pipeline_id)
            print("Message sent to the conversion queue 2")
            # Chama a task que executa o usecase da próxima etapa

        return sra_path
