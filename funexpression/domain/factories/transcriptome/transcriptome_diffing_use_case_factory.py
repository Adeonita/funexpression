from domain.usecases.transcriptome.transcriptome_diff_usecase import (
    TranscriptomeDiffUseCase,
)
from infrastructure.differs.deseq2_adapter import DESeq2Adapter
from infrastructure.reports.email_sender import EmailSender
from infrastructure.reports.report import Report
from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)
from infrastructure.storage.storage_path_adapter import StoragePathsAdapter


class DifferTranscriptomeUseCaseFactory:
    @staticmethod
    def create():
        report = Report()
        deseq2_adapter = DESeq2Adapter(report)
        email_sender = EmailSender()
        storage_paths = StoragePathsAdapter()
        pipeline_repository = PipelineRepositoryMongo()

        return TranscriptomeDiffUseCase(
            deseq2_adapter, email_sender, storage_paths, pipeline_repository
        )
