from domain.usecases.pipeline.pipeline_create_usecase import PipelineCreateUseCase
from infrastructure.messaging.task import Task
from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)


class PipelineCreateUseCaseFactory:

    @staticmethod
    def create():
        pipeline_repository = PipelineRepositoryMongo()
        task = Task()

        return PipelineCreateUseCase(task=task, pipeline_repository=pipeline_repository)
