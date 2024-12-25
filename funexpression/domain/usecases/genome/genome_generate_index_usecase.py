from domain.entities.genome import GenomeFilesEnum, GenomeStatusEnum
from domain.usecases.base_usecase import BaseUseCase
from domain.usecases.genome.input.genome_generate_index_usecase_input import (
    GenomeGenerateIndexUseCaseInput,
)
from ports.infrastructure.aligner.aligner_port import AlignerPort
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from ports.infrastructure.storage.storage_path_port import StoragePathsPort


class GenomeIndexGenerateUseCase(BaseUseCase):
    def __init__(
        self,
        aligner: AlignerPort,
        storage_paths: StoragePathsPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.aligner = aligner
        self.storage_paths = storage_paths
        self.pipeline_repository = pipeline_repository

    def execute(self, input: GenomeGenerateIndexUseCaseInput):
        self.aligner.generate_genome_index(
            genome_id=input.genome_id,
            gtf_genome_path=input.gtf_genome_path,
            fasta_genome_path=input.fasta_genome_path,
            index_genome_output_path=input.index_genome_output_path,
        )

        self.pipeline_repository.update_genome_file_status(
            pipeline_id=input.pipeline_id,
            genome_id=input.genome_id,
            file_status=GenomeStatusEnum.GENERATED,
            file=GenomeFilesEnum.INDEX,
        )

