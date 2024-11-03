from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum
from domain.usecases.base_usecase import BaseUseCase
from domain.usecases.genome.input.genome_aligner_usecase_input import (
    GenomeAlignerUseCaseInput,
)
from infrastructure.celery import count_transcriptome_task
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

        # TODO: add genome_id to the input
        genome_id = self.pipeline_repository.get_genome_id_by_pipeline(
            input.pipeline_id
        )

        genome_paths = self.storage_paths.get_genome_paths(genome_id)
        counted_transcriptome_path = self.storage_paths.get_counting_path(
            input.pipeline_id, input.organism_group, input.sra_id
        )

        count_transcriptome_task(
            pipeline_id=input.pipeline_id,
            sra_id=input.sra_id,
            organism_group=input.organism_group,
            aligned_transcriptome_path=counted_transcriptome_path.input,
            gtf_genome_path=genome_paths.gtf_path,
            counted_transcriptome_path=counted_transcriptome_path.output,
        )

        if self.pipeline_repository.is_all_sra_files_aligned(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id,
                pipeline_stage=PipelineStageEnum.ALIGNED,
            )

            print("Aligner step done!")
