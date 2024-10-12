from domain.entities.pipeline import Pipeline
from domain.usecases.base_usecase import BaseUseCase
from ports.infrastructure.messaging.task_port import TaskPort
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from infrastructure.celery import convert_sra_to_fasta_task, download_sra_task

from domain.entities.triplicate import (
    SRAFile,
    Triplicate,
    OrganinsGroupEnum,
    SRAFileStatusEnum,
)
from domain.usecases.pipeline.input.pipeline_create_input import (
    PipelineCreateUseCaseInput,
)
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from domain.usecases.conversion.input.conversion_sra_to_fasta_usecase_input import (
    ConversionSraToFastaUseCaseInput,
)
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)


class PipelineCreateUseCase(BaseUseCase):

    def __init__(
        self,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.pipeline_repository = pipeline_repository

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

                self._convert_pipeline(created_pipeline)

                return {
                    "message": f"Your pipeline is already created, and the status is: {created_pipeline.stage.value}"
                }
            # downloaded pipeline
            elif created_pipeline.stage == PipelineStageEnum.DOWNLOADED:
                self._convert_pipeline(created_pipeline)
                return {
                    "message": f"Your pipeline is already created, and are await to conversion. The actual status is {created_pipeline.stage.value}"
                }

        experiment_organism = self._get_experiment_organism(input)
        control_organism = self._get_control_organism(input)

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

    def _get_control_organism(self, input: PipelineCreateUseCaseInput):
        return Triplicate(
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

    def _get_experiment_organism(self, input: PipelineCreateUseCaseInput):
        return Triplicate(
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

    def _download_triplicate(self, tri: Triplicate, pipeline_id: str):
        self._download_sra(tri.srr_1, pipeline_id)
        self._download_sra(tri.srr_2, pipeline_id)
        self._download_sra(tri.srr_3, pipeline_id)

    def _download_sra(self, sra_file: SRAFile, pipeline_id: str):
        sra_id = sra_file.acession_number

        input = TranscriptomeDownloadUseCaseInput(sra_id, pipeline_id)
        download_sra_task(input)

    def _convert_sra_to_fasta(
        self, sra_file: SRAFile, pipeline_id: str, organism_group: str
    ):
        sra_id = sra_file.acession_number

        input = ConversionSraToFastaUseCaseInput(sra_id, pipeline_id, organism_group)
        convert_sra_to_fasta_task(input)

    def _convert_triplicate(
        self, tri: Triplicate, pipeline_id: str, organism_group: str
    ):
        self._convert_sra_to_fasta(tri.srr_1, pipeline_id, organism_group)
        self._convert_sra_to_fasta(tri.srr_2, pipeline_id, organism_group)
        self._convert_sra_to_fasta(tri.srr_3, pipeline_id, organism_group)

    def _convert_pipeline(self, pipeline: Pipeline):
        self._convert_triplicate(
            pipeline.experiment_organism, pipeline.id, OrganinsGroupEnum.EXPERIMENT
        )
        self._convert_triplicate(
            pipeline.control_organism, pipeline.id, OrganinsGroupEnum.CONTROL
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
