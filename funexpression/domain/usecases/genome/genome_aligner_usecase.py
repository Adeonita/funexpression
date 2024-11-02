from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum
from domain.usecases.base_usecase import BaseUseCase
from domain.usecases.genome.input.genome_aligner_usecase_input import (
    GenomeAlignerUseCaseInput,
)
from ports.infrastructure.aligner.aligner_port import AlignerPort
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from ports.infrastructure.storage.storage_path_port import StoragePathsPort


class GenomeAlignerUseCase(BaseUseCase):
    def __init__(
        self,
        aligner: AlignerPort,
        storage_paths: StoragePathsPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.aligner = aligner
        self.storage_paths = storage_paths
        self.pipeline_repository = pipeline_repository

    def execute(self, input: GenomeAlignerUseCaseInput):
        self.aligner.align(
            sra_id=input.sra_id,
            genome_index_path=input.genome_index_path,
            input_path=input.trimed_transcriptome_path,
            output_path=input.aligned_transcriptome_path,
        )

        self.pipeline_repository.update_sra_file_status(
            pipeline_id=input.pipeline_id,
            sra_id=input.sra_id,
            status=SRAFileStatusEnum.ALIGNED,
        )

        if self.pipeline_repository.is_all_sra_files_aligned(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id,
                pipeline_stage=PipelineStageEnum.ALIGNED,
            )

            print("Aligner step done!")
            # TODO: send message to count queue
