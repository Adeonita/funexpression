from domain.entities.de_metadata import DEMetadataStageEnum
from domain.entities.genome import Genome, GenomeFiles, GenomeStatusEnum
from domain.entities.pipeline import Pipeline
from domain.usecases.base_usecase import BaseUseCase
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.usecases.pipeline.pipeline_gateway import PipelineGateway


from domain.entities.triplicate import (
    SRAFile,
    Triplicate,
    SRAFileStatusEnum,
)
from domain.usecases.pipeline.input.pipeline_create_input import (
    PipelineCreateUseCaseInput,
)
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from ports.infrastructure.storage.storage_path_port import StoragePathsPort


class PipelineCreateUseCase(BaseUseCase):

    def __init__(
        self,
        pipeline_repository: PipelineRepositoryPort,
        storage_paths: StoragePathsPort,
        pipeline_gateway: PipelineGateway,
    ):
        self.pipeline_repository = pipeline_repository
        self.storage_paths = storage_paths
        self.pipeline_gateway = pipeline_gateway

    def execute(self, input: PipelineCreateUseCaseInput):
        created_pipeline = self._find_pipeline(input)

        if created_pipeline:
            created_pipeline = Pipeline.from_json(created_pipeline)
            return self.pipeline_gateway.handle(created_pipeline)

        experiment_organism = self._get_experiment_organism(input)
        control_organism = self._get_control_organism(input)
        reference_genome = self._get_reference_genome(input)

        pipeline: Pipeline = self.pipeline_repository.create(
            name=input.name,
            email=input.email,
            run_id=input.run_id,
            stage=PipelineStageEnum.PENDING,
            experiment_organism=experiment_organism,
            control_organism=control_organism,
            reference_genome=reference_genome,
            p_adj=input.p_adj,
            log_2_fold_change_threshold=input.log_2_fold_change_threshold,
        )

        self.storage_paths.create_pipeline_directory_structure(pipeline_id=pipeline.id)

        self.pipeline_gateway.start(pipeline)
        return pipeline

    def _get_reference_genome(self, input: PipelineCreateUseCaseInput) -> Genome:
        return Genome(
            acession_number=input.reference_genome_acession_number,
            state=GenomeStatusEnum.PENDING,
            genome_files=GenomeFiles(
                gtf=GenomeStatusEnum.PENDING,
                fasta=GenomeStatusEnum.PENDING,
                index=GenomeStatusEnum.PENDING,
            ),
        )

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

        if len(pipelines) > 0:
            pipeline = pipelines[0]

            return pipeline

        return None
