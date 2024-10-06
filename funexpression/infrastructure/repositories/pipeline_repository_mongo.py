from typing import List
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

    def get(self, id: str) -> Pipeline:
        raw_pipeline = self.database.get_by_id("pipelines", id)
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
            "control_organism": {
                "srr_1": {
                    "acession_number": control_organism[0],
                    "status": SRAFileStatusEnum.PENDING.value,
                },
                "srr_2": {
                    "acession_number": control_organism[1],
                    "status": SRAFileStatusEnum.PENDING.value,
                },
                "srr_3": {
                    "acession_number": control_organism[2],
                    "status": SRAFileStatusEnum.PENDING.value,
                },
            },
            "experiment_organism": {
                "srr_1": {
                    "acession_number": experiment_organism[0],
                    "status": SRAFileStatusEnum.PENDING.value,
                },
                "srr_2": {
                    "acession_number": experiment_organism[1],
                    "status": SRAFileStatusEnum.PENDING.value,
                },
                "srr_3": {
                    "acession_number": experiment_organism[2],
                    "status": SRAFileStatusEnum.PENDING.value,
                },
            },
            "reference_genome_acession_number": reference_genome_acession_number,
        }

        pipelines = self.database.find("pipelines", query)

        return pipelines

    def is_all_file_download_completed(self, pipeline_id: str) -> bool:
        pipeline = self.get(pipeline_id)

        if not pipeline:
            raise Exception("Pipeline not found")

        control_organism_ready = (
            pipeline.control_organism.srr_1.status == SRAFileStatusEnum.OK
            and pipeline.control_organism.srr_2.status == SRAFileStatusEnum.OK
            and pipeline.control_organism.srr_3.status == SRAFileStatusEnum.OK
        )

        experiment_organism_ready = (
            pipeline.experiment_organism.srr_1.status == SRAFileStatusEnum.OK
            and pipeline.experiment_organism.srr_2.status == SRAFileStatusEnum.OK
            and pipeline.experiment_organism.srr_3.status == SRAFileStatusEnum.OK
        )

        return control_organism_ready and experiment_organism_ready
