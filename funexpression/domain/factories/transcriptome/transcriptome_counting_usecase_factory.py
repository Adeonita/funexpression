from domain.usecases.transcriptome.transciptome_count_usecase import (
    TranscriptomeCountUseCase,
)
from infrastructure.counters.htseq_count import HTSeqCountAdapter
from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)
from infrastructure.storage.storage_path_adapter import StoragePathsAdapter


class TranscriptomeCountingUseCaseFactory:

    @staticmethod
    def create():
        counter_adapter = HTSeqCountAdapter()
        storage_paths = StoragePathsAdapter()
        pipeline_repository = PipelineRepositoryMongo()

        return TranscriptomeCountUseCase(
            counter_adapter, storage_paths, pipeline_repository
        )
