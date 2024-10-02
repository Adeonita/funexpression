from domain.entities.pipeline import Pipeline
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum, SRAFile, Triplicate
from domain.usecases.pipeline.input.pipeline_create_input import (
    PipelineCreateUseCaseInput,
)
from ports.infrastructure.messaging.task_port import TaskPort
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)


class PipelineCreateUseCase:

    def __init__(self, pipeline_repository: PipelineRepositoryPort, task: TaskPort):
        self.pipeline_repository = pipeline_repository
        self.task = task

    def execute(self, input: PipelineCreateUseCaseInput):
        created_pipeline = self._find_pipeline(input)

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
                # dispara o usecase de conversão via task
            print(
                f"Pipeline already exist with stage:  {created_pipeline.stage.value}"
            )  # retorna alguma coisa pro usuário avisando
            return

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
        self.task.sra_transcriptome_download.delay(
            sra_id=sra_file.acession_number,
            pipeline_id=pipeline_id,
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
