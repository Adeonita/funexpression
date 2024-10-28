from domain.usecases.genome.genome_download_usecase import GenomeDownloadUseCase
from infrastructure.bio_database.genbank_adapter import GenBankAdapter

from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)
from infrastructure.storage.storage_path_adapter import StoragePathsAdapter


class GenomeDownloadUseCaseFactory:

    @staticmethod
    def create():
        genbank_adapter = GenBankAdapter()
        storage_paths = StoragePathsAdapter()
        pipeline_repository = PipelineRepositoryMongo()

        return GenomeDownloadUseCase(
            genbank_adapter, storage_paths, pipeline_repository
        )
