from domain.usecases.genome.genome_download_usecase import GenomeDownloadUseCase
from infrastructure.bio_database.genbank_adapter import GenBankAdapter

from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)


class GenomeDownloadUseCaseFactory:

    @staticmethod
    def create():
        genbank_adapter = GenBankAdapter()
        pipeline_repository = PipelineRepositoryMongo()

        return GenomeDownloadUseCase(genbank_adapter, pipeline_repository)
