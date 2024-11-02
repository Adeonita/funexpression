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
        pipeline_gateway = PipelineGateway(pipeline_repository=pipeline_repository)

        return PipelineCreateUseCase(
            pipeline_repository=pipeline_repository,
            storage_paths=storage_paths,
            pipeline_gateway=pipeline_gateway,
        )
