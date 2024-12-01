from domain.entities.pipeline_stage_enum import PipelineStageEnum
from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)


def set_pipeline_status_to_failed(pipeline_id: str):
    pipeline_repository = PipelineRepositoryMongo()
    pipeline_repository.update_status_to_task(pipeline_id, PipelineStageEnum.FAILED)
