from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)
from domain.usecases.transcriptome.transcriptome_trimming_usecase import (
    TranscriptomeTrimming,
)
from infrastructure.storage.storage_path_adapter import StoragePathsAdapter
from infrastructure.trimmers.trimmomatic_adapter import TrimmomaticAdapter


class TranscriptomeTrimmingUseCaseFactory:

    @staticmethod
    def create():
        trimmer = TrimmomaticAdapter()
        storage_paths = StoragePathsAdapter()
        pipeline_repository = PipelineRepositoryMongo()

        return TranscriptomeTrimming(trimmer, storage_paths, pipeline_repository)
