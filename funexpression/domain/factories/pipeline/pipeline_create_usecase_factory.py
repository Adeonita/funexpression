from domain.tasks.genome.genome_download_task import GenomeDownloadTask
from domain.tasks.pipeline_task import PipelineTask
from domain.tasks.transcriptome.transcriptome_align_task import TranscripomeAlignTask
from domain.tasks.transcriptome.transcriptome_convert_task import TranscripomeConvertTask
from domain.tasks.transcriptome.transcriptome_download_task import TranscriptomeDownloadTask
from domain.tasks.transcriptome.transcriptome_trim import TranscriptomeTrimTask
from domain.usecases.pipeline.pipeline_create_usecase import PipelineCreateUseCase
from domain.usecases.pipeline.pipeline_gateway import PipelineGateway
from infrastructure.messaging.task import Task
from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)
from infrastructure.storage.storage_path_adapter import StoragePathsAdapter


class PipelineCreateUseCaseFactory:

    @staticmethod
    def create():
        storage_paths = StoragePathsAdapter()
        pipeline_repository = PipelineRepositoryMongo()
        transcriptome_align_task = TranscripomeAlignTask(storage_paths=storage_paths)
        genome_download_task = GenomeDownloadTask()
        transcriptome_download_task = TranscriptomeDownloadTask()
        transcriptome_convert_task = TranscripomeConvertTask()
        transcriptome_trim_task = TranscriptomeTrimTask(storage_paths=storage_paths)

        pipeline_task = PipelineTask(genome_download_task, transcriptome_download_task, transcriptome_convert_task, transcriptome_trim_task,  transcriptome_align_task)
        pipeline_gateway = PipelineGateway(
            pipeline_repository=pipeline_repository, pipeline_task=pipeline_task
        )

        return PipelineCreateUseCase(
            pipeline_repository=pipeline_repository,
            storage_paths=storage_paths,
            pipeline_gateway=pipeline_gateway,
        )
