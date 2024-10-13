from typing import List
from bson import ObjectId
from domain.entities.pipeline import Pipeline
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum, Triplicate
from infrastructure.database.mongo_adapter import MongoAdapter
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)


class PipelineRepositoryMongo(PipelineRepositoryPort):
    database: MongoAdapter

    def __init__(self):
        self.database = MongoAdapter()

    def create(
        self,
        email: str,
        run_id: str,
        stage: PipelineStageEnum,
        control_organism: Triplicate,
        experiment_organism: Triplicate,
        reference_genome_acession_number: str,
    ) -> Pipeline:
        pipeline = Pipeline(
            email=email,
            run_id=run_id,
            stage=stage,
            control_organism=control_organism,
            experiment_organism=experiment_organism,
            reference_genome_acession_number=reference_genome_acession_number,
        )

        pipeline_id = self.database.create("pipelines", pipeline.to_json())
        pipeline.id = str(pipeline_id)

        return pipeline

    def get(self, pipeline_id: str) -> Pipeline:
        raw_pipeline = self.database.get_by_id("pipelines", pipeline_id)
        pipeline = None
        try:
            pipeline = Pipeline.from_json(raw_pipeline)
        except Exception as e:
            print(f"from json error: {e}")

        if not pipeline:
            raise Exception("Get Pipeline: Pipeline not found")
        return pipeline

    def update_status(self, pipeline_id: int, pipeline_stage: PipelineStageEnum):
        pipeline = self.get(pipeline_id)

        if not pipeline:
            raise Exception("Get Pipeline: Pipeline not found")

        pipeline.stage = pipeline_stage
        self.database.updateById(pipeline_id, pipeline.to_json())

    def update_sra_file_status(
        self, pipeline_id: int, sra_id: str, status: SRAFileStatusEnum
    ):
        pipeline = self.get(pipeline_id)

        try:
            # Control
            if pipeline.control_organism.srr_1.acession_number == sra_id:
                self.database.updateById(
                    pipeline_id, {"control_organism.srr_1.status": status}
                )
                return

            if pipeline.control_organism.srr_2.acession_number == sra_id:
                self.database.updateById(
                    pipeline_id, {"control_organism.srr_2.status": status}
                )
                return

            if pipeline.control_organism.srr_3.acession_number == sra_id:
                self.database.updateById(
                    pipeline_id, {"control_organism.srr_3.status": status}
                )
                return

            # Experiment
            if pipeline.experiment_organism.srr_1.acession_number == sra_id:
                self.database.updateById(
                    pipeline_id, {"experiment_organism.srr_1.status": status}
                )
                return

            if pipeline.experiment_organism.srr_2.acession_number == sra_id:
                self.database.updateById(
                    pipeline_id, {"experiment_organism.srr_2.status": status}
                )
                return

            if pipeline.experiment_organism.srr_3.acession_number == sra_id:
                self.database.updateById(
                    pipeline_id, {"experiment_organism.srr_3.status": status}
                )
                return

        except Exception as e:
            print(f"update sra file status error: --> {str(e)}")

    def find_pipeline(
        self,
        email: str,
        control_organism: List[str],
        experiment_organism: List[str],
        reference_genome_acession_number: str,
    ):
        query = {
            "email": email,
            "control_organism.srr_1.acession_number": control_organism[0],
            "control_organism.srr_2.acession_number": control_organism[1],
            "control_organism.srr_3.acession_number": control_organism[2],
            "experiment_organism.srr_1.acession_number": experiment_organism[0],
            "experiment_organism.srr_2.acession_number": experiment_organism[1],
            "experiment_organism.srr_3.acession_number": experiment_organism[2],
            "reference_genome_acession_number": reference_genome_acession_number,
        }

        pipelines = self.database.find("pipelines", query)

        return pipelines

    def _get_pipeline_by_sra_state(
        self, pipeline_id: str, sra_status: SRAFileStatusEnum
    ):

        query = {
            "_id": ObjectId(pipeline_id),
            "control_organism.srr_1.status": sra_status,
            "control_organism.srr_2.status": sra_status,
            "control_organism.srr_3.status": sra_status,
            "experiment_organism.srr_1.status": sra_status,
            "experiment_organism.srr_2.status": sra_status,
            "experiment_organism.srr_3.status": sra_status,
        }

        pipeline = self.database.find("pipelines", query)

        if not pipeline:
            return False

        control = pipeline[0]["control_organism"]
        experiment = pipeline[0]["experiment_organism"]

        control_organism = (
            control["srr_1"]["status"],
            control["srr_2"]["status"],
            control["srr_3"]["status"],
        )

        experiment_organism = (
            experiment["srr_1"]["status"],
            experiment["srr_2"]["status"],
            experiment["srr_3"]["status"],
        )

        return control_organism and experiment_organism

    def is_all_file_download_converted(self, pipeline_id: str) -> bool:
        result = self._get_pipeline_by_sra_state(
            pipeline_id, SRAFileStatusEnum.CONVERTED.value
        )

        return True if result else False

    def is_all_file_download_downloaded(self, pipeline_id: str) -> bool:
        result = self._get_pipeline_by_sra_state(
            pipeline_id, SRAFileStatusEnum.DOWNLOADED.value
        )

        return True if result else False

    def get_sra_files(self, pipeline_id: str) -> List[str]:
        pipeline = self.get(pipeline_id)

        if not pipeline:
            raise Exception("Pipeline not found")

        result = {
            "control": [
                pipeline.control_organism.srr_1.acession_number,
                pipeline.control_organism.srr_2.acession_number,
                pipeline.control_organism.srr_3.acession_number,
            ],
            "experiment": [
                pipeline.experiment_organism.srr_1.acession_number,
                pipeline.experiment_organism.srr_2.acession_number,
                pipeline.experiment_organism.srr_3.acession_number,
            ],
        }

        return result
