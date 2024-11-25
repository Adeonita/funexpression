from typing import List, Protocol
from application.interfaces.expression_request_payload import Triplicate
from domain.entities.de_metadata import DEMetadataStageEnum
from domain.entities.genome import Genome, GenomeFilesEnum, GenomeStatusEnum
from domain.entities.pipeline import Pipeline
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum


class PipelineRepositoryPort(Protocol):

    def create(
        self,
        name: str,
        email: str,
        run_id: str,
        stage: PipelineStageEnum,
        control_organism: Triplicate,
        experiment_organism: Triplicate,
        reference_genome_acession_number: Genome,
        p_adj: float,
        log_2_fold_change_threshold: float,
    ) -> Pipeline:
        pass

    def get(self, pipeline_id: str) -> Pipeline:
        pass

    def update_sra_file_status(
        self, pipeline_id: int, sra_id: str, status: SRAFileStatusEnum
    ):
        pass

    def update_status(self, pipeline_id: int, pipeline_stage: PipelineStageEnum):
        pass

    def update_genome_file_status(
        self,
        pipeline_id: int,
        genome_id: str,
        file_status: GenomeStatusEnum,
        file: GenomeFilesEnum,
    ):
        pass

    def update_genome_reference_status(
        self, pipeline_id: str, genome_id: str, status: GenomeStatusEnum
    ):
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

    def is_all_sra_files_aligned(self, pipeline_id: str) -> bool:
        pass

    def is_all_sra_files_counted(self, pipeline_id: str) -> bool:
        pass

    def is_all_sra_files_diffed(self, pipeline_id: str) -> bool:
        pass

    def get_sra_files(self, pipeline_id: str) -> dict:
        pass

    def get_genome_id_by_pipeline(self, pipeline_id: str) -> str:
        pass

    def get_user_data(pipeline_id) -> dict:
        pass

    def get_p_adj_by_pipeline(self, pipeline_id: str) -> float:
        pass

    def get_log_2_fold_change_threshold_by_pipeline(self, pipeline_id: str) -> float:
        pass

    def get_pipeline_info(self, pipeline_id: str) -> dict:
        pass
