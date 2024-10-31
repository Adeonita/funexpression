from domain.usecases.genome.genome_aligner_usecase import GenomeAlignerUseCase
from infrastructure.aligners.rna_star_adapter import RnaStarAdapter
from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)
from infrastructure.storage.storage_path_adapter import StoragePathsAdapter


class GenomeAlignerUseCaseFactory:
    @staticmethod
    def create():
        rna_star_adapter = RnaStarAdapter()
        storage_paths = StoragePathsAdapter()
        pipeline_repository = PipelineRepositoryMongo()

        return GenomeAlignerUseCase(
            rna_star_adapter, storage_paths, pipeline_repository
        )
