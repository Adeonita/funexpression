from domain.usecases.transcriptome.transcriptome_diff_usecase import (
    TranscriptomeDiffUseCase,
)
from infrastructure.differs.deseq2_adapter import DESeq2Adapter
from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)
from infrastructure.storage.storage_path_adapter import StoragePathsAdapter


class DifferTranscriptomeUseCaseFactory:
    @staticmethod
    def create():
        deseq2_adapter = DESeq2Adapter()
        storage_paths = StoragePathsAdapter()
        pipeline_repository = PipelineRepositoryMongo()

        return TranscriptomeDiffUseCase(
            deseq2_adapter, storage_paths, pipeline_repository
        )
