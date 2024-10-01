import json
from domain.entities.pipeline import Pipeline
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum, Triplicate
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from uuid import uuid4
from pysondb import db

pipelines_datasources = db.getDb("db.json")


class PipelineRepository(PipelineRepositoryPort):

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
            id=str(uuid4()),
            email=email,
            run_id=run_id,
            stage=stage,
            control_organism=control_organism,
            experiment_organism=experiment_organism,
            reference_genome_acession_number=reference_genome_acession_number,
        )

        pipelines_datasources.add(pipeline.to_json())

        return pipeline

    def get(self, id: str) -> Pipeline:
        pipeline = Pipeline.from_json(pipelines_datasources.getBy({"id", id}))

        if not pipeline:
            raise Exception("Get Pipeline: Pipeline not found")
        return pipeline

    def update_sra_file_status(
        self, pipeline_id: int, sra_id: str, status: SRAFileStatusEnum
    ):
        pipeline = self.get(pipeline_id)

        # Control
        if pipeline.control_organism.srr_1.acession_number == sra_id:
            pipeline.control_organism.srr_1.status = status

        if pipeline.control_organism.srr_2.acession_number == sra_id:
            pipeline.control_organism.srr_2.status = status

        if pipeline.control_organism.srr_3.acession_number == sra_id:
            pipeline.control_organism.srr_3.status = status

        # Experiment
        if pipeline.experiment_organism.srr_1.acession_number == sra_id:
            pipeline.experiment_organism.srr_1.status = status

        if pipeline.experiment_organism.srr_2.acession_number == sra_id:
            pipeline.experiment_organism.srr_2.status = status

        if pipeline.experiment_organism.srr_3.acession_number == sra_id:
            pipeline.experiment_organism.srr_3.status = status

        pipelines_datasources.updateByQuery({"id": pipeline_id}, pipeline.to_json())

        print(f"pipeline {pipeline_id} updated {sra_id} to {str(status)}")
