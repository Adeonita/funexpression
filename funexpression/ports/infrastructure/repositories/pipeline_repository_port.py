from typing import Protocol
from domain.entities.pipeline import Pipeline
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum


class PipelineRepositoryPort(Protocol):

    def create(self, email: str, run_id: str, stage: PipelineStageEnum) -> Pipeline:
        pass

    def get(self, run_id: str) -> Pipeline:
        pass

    def update_sra_file_status(
        self, pipeline_id: int, sra_id: str, status: SRAFileStatusEnum
    ):
        pass
