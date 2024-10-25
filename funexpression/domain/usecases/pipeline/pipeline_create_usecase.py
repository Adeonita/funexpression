from domain.entities.genome import Genome, GenomeFiles, GenomeStatusEnum
from domain.entities.pipeline import Pipeline
from domain.usecases.base_usecase import BaseUseCase
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from infrastructure.celery import (
    convert_sra_to_fasta_task,
    download_genome_task,
    download_sra_task,
)

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


class PipelineCreateUseCase(BaseUseCase):

    def __init__(
        self,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.pipeline_repository = pipeline_repository

    def execute(self, input: PipelineCreateUseCaseInput):
        created_pipeline = self._find_pipeline(input)

        if created_pipeline:
            created_pipeline = Pipeline.from_json(created_pipeline)
            sra_files_download_completed = (
                self.pipeline_repository.is_all_file_download_downloaded(
                    created_pipeline.id
                )
            )

            pipeline_sra_files_download_pending = (
                created_pipeline.stage == PipelineStageEnum.PENDING
                and not sra_files_download_completed
            )

            if pipeline_sra_files_download_pending:
                return {
                    "message": "Your pipeline is awaiting download the sra files, please wait a moment",
                    "pipeline_stage": created_pipeline.stage.value,
                }
                # I will should be some thing?

            pipeline_files_downloaded = (
                created_pipeline.stage == PipelineStageEnum.PENDING
                and sra_files_download_completed
            )

            pipeline_sra_files_read_to_convert = (
                created_pipeline.stage == PipelineStageEnum.DOWNLOADED
                and sra_files_download_completed
            )

            if pipeline_files_downloaded:
                self.pipeline_repository.update_status(
                    created_pipeline.id, PipelineStageEnum.DOWNLOADED
                )

                self._convert_transcriptomes(created_pipeline)

                return {
                    "message": f"Your pipeline is already created, and the sra files are awaiting was sent to conversion",
                    "pipeline_stage": created_pipeline.stage.value,
                }
            # downloaded pipeline
            elif pipeline_sra_files_read_to_convert:
                self._convert_transcriptomes(created_pipeline)
                return {
                    "message": f"Your pipeline is already created, and are await to conversion.",
                    "pipeline_stage": created_pipeline.stage.value,
                }
            # elif created_pipeline.stage == PipelineStageEnum.CONVERTED:
            #     self._trimming_transcriptomes(created_pipeline)
            # elif created_pipeline.stage == PipelineStageEnum.TRIMMED:
            #     self._align_transcriptomes(created_pipeline)
            # elif created_pipeline.stage == PipelineStageEnum.ALIGNED:
            #     self._normalize_transcriptomes(created_pipeline)
            # elif created_pipeline.stage == PipelineStageEnum.COUNTED:
            #     self._differential_expression(created_pipeline)
            # elif created_pipeline.stage == PipelineStageEnum.DIFFERENTIAL_EXPRESSION:
            #     self._send_email(created_pipeline)

        experiment_organism = self._get_experiment_organism(input)
        control_organism = self._get_control_organism(input)
        reference_genome = self._get_reference_genome(input)

        pipeline: Pipeline = self.pipeline_repository.create(
            email=input.email,
            run_id=input.run_id,
            stage=PipelineStageEnum.PENDING,
            experiment_organism=experiment_organism,
            control_organism=control_organism,
            reference_genome=reference_genome,
        )

        # self._download_transcriptomes(pipeline)
        self._download_genome_and_transcriptome(pipeline)

        return pipeline

    def _get_reference_genome(self, input: PipelineCreateUseCaseInput) -> Genome:
        return Genome(
            acession_number=input.reference_genome_acession_number,
            state=GenomeStatusEnum.PENDING,
            genome_files=GenomeFiles(
                gtf=GenomeStatusEnum.PENDING,
                fasta=GenomeStatusEnum.PENDING,
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

    def _download_genome_and_transcriptome(self, pipeline: Pipeline):
        self._download_genome(pipeline)
        self._download_transcriptomes(pipeline)

        return

    def _download_genome(self, pipeline: Pipeline):
        download_genome_task(
            genome_id=pipeline.reference_genome.acession_number, pipeline_id=pipeline.id
        )

    def _download_transcriptomes(self, pipeline: Pipeline):
        self._download_triplicate(
            pipeline.control_organism, pipeline.id, OrganinsGroupEnum.CONTROL
        )

        self._download_triplicate(
            pipeline.experiment_organism, pipeline.id, OrganinsGroupEnum.EXPERIMENT
        )

    def _download_triplicate(
        self, tri: Triplicate, pipeline_id: str, organism_group: OrganinsGroupEnum
    ):
        self._download_sra(tri.srr_1, pipeline_id, organism_group)
        self._download_sra(tri.srr_2, pipeline_id, organism_group)
        self._download_sra(tri.srr_3, pipeline_id, organism_group)

    def _download_sra(
        self, sra_file: SRAFile, pipeline_id: str, organism_group: OrganinsGroupEnum
    ):
        sra_id = sra_file.acession_number

        download_sra_task(sra_id, pipeline_id, organism_group)

    def _convert_sra_to_fasta(
        self, sra_file: SRAFile, pipeline_id: str, organism_group: str
    ):
        sra_id = sra_file.acession_number

        convert_sra_to_fasta_task(sra_id, pipeline_id, organism_group)

    def _convert_triplicate(
        self, tri: Triplicate, pipeline_id: str, organism_group: str
    ):
        self._convert_sra_to_fasta(tri.srr_1, pipeline_id, organism_group)
        self._convert_sra_to_fasta(tri.srr_2, pipeline_id, organism_group)
        self._convert_sra_to_fasta(tri.srr_3, pipeline_id, organism_group)

    def _convert_transcriptomes(self, pipeline: Pipeline):
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

        if len(pipelines) > 0:
            pipeline = pipelines[0]

            return Pipeline(
                id=str(pipeline["_id"]),
                run_id=pipeline["run_id"],
                email=pipeline["email"],
                stage=PipelineStageEnum(pipeline["stage"]),
                control_organism=Triplicate(
                    srr_1=SRAFile(
                        acession_number=pipeline["control_organism"]["srr_1"][
                            "acession_number"
                        ],
                        status=SRAFileStatusEnum[
                            pipeline["control_organism"]["srr_1"]["status"]
                        ],
                    ),
                    srr_2=SRAFile(
                        acession_number=pipeline["control_organism"]["srr_2"][
                            "acession_number"
                        ],
                        status=SRAFileStatusEnum[
                            pipeline["control_organism"]["srr_2"]["status"]
                        ],
                    ),
                    srr_3=SRAFile(
                        acession_number=pipeline["control_organism"]["srr_3"][
                            "acession_number"
                        ],
                        status=SRAFileStatusEnum[
                            pipeline["control_organism"]["srr_3"]["status"]
                        ],
                    ),
                ),
                experiment_organism=Triplicate(
                    srr_1=SRAFile(
                        acession_number=pipeline["experiment_organism"]["srr_1"][
                            "acession_number"
                        ],
                        status=SRAFileStatusEnum[
                            pipeline["experiment_organism"]["srr_1"]["status"]
                        ],
                    ),
                    srr_2=SRAFile(
                        acession_number=pipeline["experiment_organism"]["srr_2"][
                            "acession_number"
                        ],
                        status=SRAFileStatusEnum[
                            pipeline["experiment_organism"]["srr_2"]["status"]
                        ],
                    ),
                    srr_3=SRAFile(
                        acession_number=pipeline["experiment_organism"]["srr_3"][
                            "acession_number"
                        ],
                        status=SRAFileStatusEnum[
                            pipeline["experiment_organism"]["srr_3"]["status"]
                        ],
                    ),
                ),
                reference_genome=Genome(
                    acession_number=pipeline["reference_genome"]["acession_number"],
                    state=GenomeStatusEnum[pipeline["reference_genome"]["status"]],
                    genome_files=GenomeFiles(
                        gtf=GenomeStatusEnum[
                            pipeline["reference_genome"]["genome_files"]["gtf"]
                        ],
                        fasta=GenomeStatusEnum[
                            pipeline["reference_genome"]["genome_files"]["fasta"]
                        ],
                    ),
                ),
            )

        return None
