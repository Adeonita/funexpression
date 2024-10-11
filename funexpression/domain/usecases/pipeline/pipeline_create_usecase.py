from domain.entities.pipeline import Pipeline
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum, SRAFile, Triplicate
from domain.usecases.base_usecase import BaseUseCase
from domain.usecases.pipeline.input.pipeline_create_input import (
    PipelineCreateUseCaseInput,
)
from ports.infrastructure.messaging.task_port import TaskPort
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from infrastructure.celery import app


class PipelineCreateUseCase(BaseUseCase):

    def __init__(
        self,
        task: TaskPort,  # TODO: remover task dependency from this class and your respective factory
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.pipeline_repository = pipeline_repository
        self.task = task

    def execute(self, input: PipelineCreateUseCaseInput):
        created_pipeline = self._find_pipeline(input)  # pending pipeline

        if created_pipeline:
            created_pipeline = Pipeline.from_json(created_pipeline)
            if (
                created_pipeline.stage == PipelineStageEnum.PENDING
                and self.pipeline_repository.is_all_file_download_completed(
                    created_pipeline.id
                )
            ):
                self.pipeline_repository.update_status(
                    created_pipeline.id, PipelineStageEnum.DOWNLOADED
                )
                print("Enviando para conversão")

                app.send_task(
                    "infrastructure.messaging.task.sra_to_fasta_conversion",
                    args=(created_pipeline.id,),
                    queue="sra_to_fasta_conversion",
                )

                print("Message sending to the conversion queue")

            return {
                "message": f"Your pipeline is already created, and the status is: {created_pipeline.stage.value}"
            }

        # TODO: verificar se o pipeline já foi criado e está com download ok, pendente de conversão
        # created_downloaded_pipeline = self._find_pipeline(input)  # pipeline com download ok enviar pra converter

        experiment_organism = Triplicate(
            srr_1=SRAFile(
                acession_number=input.experiment_organism.srr_acession_number_1,
                status=SRAFileStatusEnum.PENDING,
            ),
            srr_2=SRAFile(
                acession_number=input.experiment_organism.srr_acession_number_2,
                status=SRAFileStatusEnum.PENDING,
            ),
            srr_3=SRAFile(
                acession_number=input.experiment_organism.srr_acession_number_3,
                status=SRAFileStatusEnum.PENDING,
            ),
        )

        control_organism = Triplicate(
            srr_1=SRAFile(
                acession_number=input.control_organism.srr_acession_number_1,
                status=SRAFileStatusEnum.PENDING,
            ),
            srr_2=SRAFile(
                acession_number=input.control_organism.srr_acession_number_2,
                status=SRAFileStatusEnum.PENDING,
            ),
            srr_3=SRAFile(
                acession_number=input.control_organism.srr_acession_number_3,
                status=SRAFileStatusEnum.PENDING,
            ),
        )

        pipeline: Pipeline = self.pipeline_repository.create(
            email=input.email,
            run_id=input.run_id,
            stage=PipelineStageEnum.PENDING,
            experiment_organism=experiment_organism,
            control_organism=control_organism,
            reference_genome_acession_number=input.reference_genome_acession_number,
        )

        self._download_triplicate(experiment_organism, pipeline.id)
        self._download_triplicate(control_organism, pipeline.id)

        return pipeline

    def _download_triplicate(self, tri: Triplicate, pipeline_id: str):
        self._download_sra(tri.srr_1, pipeline_id)
        self._download_sra(tri.srr_2, pipeline_id)
        self._download_sra(tri.srr_3, pipeline_id)

    def _download_sra(self, sra_file: SRAFile, pipeline_id: str):
        sra_id = sra_file.acession_number

        app.send_task(
            "infrastructure.messaging.task.sra_transcriptome_download",
            args=(sra_id, pipeline_id),
            queue="geo_sra_download",
        )

    def _find_pipeline(self, input: PipelineCreateUseCaseInput):
        pipelines = self.pipeline_repository.find_pipeline(
            email=input.email,
            control_organism=[
                input.control_organism.srr_acession_number_1,
                input.control_organism.srr_acession_number_2,
                input.control_organism.srr_acession_number_3,
            ],
            experiment_organism=[
                input.experiment_organism.srr_acession_number_1,
                input.experiment_organism.srr_acession_number_2,
                input.experiment_organism.srr_acession_number_3,
            ],
            reference_genome_acession_number=input.reference_genome_acession_number,
        )

        return pipelines[0] if len(pipelines) > 0 else None
