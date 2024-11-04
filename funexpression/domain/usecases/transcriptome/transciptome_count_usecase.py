from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum
from domain.usecases.transcriptome.input.counting_transcriptome_usecase import (
    TranscriptomeCountUseCaseInput,
)
from ports.infrastructure.counter.counter_port import CounterPort
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from ports.infrastructure.storage.storage_path_port import StoragePathsPort


class TranscriptomeCountUseCase:
    def __init__(
        self,
        counter: CounterPort,
        storage_paths: StoragePathsPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.counter_port = counter
        self.storage_paths = storage_paths
        self.pipeline_repository = pipeline_repository

    def execute(self, input: TranscriptomeCountUseCaseInput):
        self.counter_port.count(
            aligned_file_path=input.aligned_transcriptome_path,
            gtf_genome_file_path=input.gtf_genome_file_path,
            counted_file_path=input.counted_transcriptome_path,
            sra_id=input.sra_id,
        )

        self.pipeline_repository.update_sra_file_status(
            pipeline_id=input.pipeline_id,
            sra_id=input.sra_id,
            status=SRAFileStatusEnum.COUNTED,
        )

        if self.pipeline_repository.is_all_sra_files_counted(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id,
                pipeline_stage=PipelineStageEnum.COUNTED,
            )
            print("Count step done")

            print("Sending to the DE queue...")

            # TODO: enviar para fila do DE, apenas quando tiver todos os arquivos contados
        return input.counted_transcriptome_path
