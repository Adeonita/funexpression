from typing import List, Protocol
from domain.entities.pipeline import Pipeline
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum


class PipelineRepositoryPort(Protocol):

    def create(self, email: str, run_id: str, stage: PipelineStageEnum) -> Pipeline:
        pass

    def get(self, pipeline_id: str) -> Pipeline:
        pass

    def update_sra_file_status(
        self, pipeline_id: int, sra_id: str, status: SRAFileStatusEnum
    ):
        pass

    def update_status(self, pipeline_id: int, pipeline_stage: PipelineStageEnum):
        pass

    def find_pipeline(
        self,
        email: str,
        control_organism: List[str],
        experiment_organism: List[str],
        reference_genome_acession_number: str,
    ) -> List[Pipeline]:
        pass

    def is_all_file_download_downloaded(self, pipeline_id: str) -> bool:
        pass

    def is_all_file_download_converted(self, pipeline_id: str) -> bool:
        pass

    def is_all_sra_files_trimmed(self, pipeline_id: str) -> bool:
        pass

    def get_sra_files(self, pipeline_id: str) -> dict:
        pass
