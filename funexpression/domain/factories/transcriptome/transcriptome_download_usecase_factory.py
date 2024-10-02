from domain.usecases.transcriptome.transcriptome_download_usecase import (
    TranscriptomeDownloadUseCase,
)
from infrastructure.bio_database.geo_adapter import GeoAdapter
from infrastructure.repositories.pipeline_repository import PipelineRepository


class TranscriptomeDownloadUseCaseFactory:

    @staticmethod
    def create():
        geo_adapter = GeoAdapter()
        pipeline_repository = PipelineRepository()

        return TranscriptomeDownloadUseCase(geo_adapter, pipeline_repository)
