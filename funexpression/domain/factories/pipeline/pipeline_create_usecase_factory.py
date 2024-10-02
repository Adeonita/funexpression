from domain.usecases.pipeline.pipeline_create_usecase import PipelineCreateUseCase
from infrastructure.messaging.task import Task
from infrastructure.repositories.pipeline_repository import PipelineRepository


class PipelineCreateUseCaseFactory:

    @staticmethod
    def create():
        pipeline_repository = PipelineRepository()
        task = Task()

        return PipelineCreateUseCase(task=task, pipeline_repository=pipeline_repository)
