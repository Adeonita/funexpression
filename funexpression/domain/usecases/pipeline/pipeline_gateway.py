from domain.entities.de_metadata import DEMetadataStageEnum
from domain.entities.genome import GenomeStatusEnum
from domain.entities.pipeline import Pipeline
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)


class PipelineGateway:

    def __init__(self, pipeline_repository: PipelineRepositoryPort):
        self.pipeline_repository = pipeline_repository

    def handle(self, pipeline: Pipeline):

        if self._is_ready_to_converter(pipeline):
            return {
                "message": f"Your pipeline is already created, and the sra files are awaiting was sent to conversion",
                "pipeline_stage": pipeline.stage.value,
            }

        if self._is_ready_to_trim(pipeline):
            return {
                "message": f"Your pipeline is already created, and are await to trim.",
                "pipeline_stage": pipeline.stage.value,
            }

        if self._is_ready_to_aling(pipeline):
            return {
                "message": f"Your pipeline is already created, and are await to alignment.",
                "pipeline_stage": pipeline.stage.value,
            }

        if self._is_ready_to_count(pipeline):
            return {
                "message": f"Your pipeline is already created, and are await to count.",
                "pipeline_stage": pipeline.stage.value,
            }

        if self._is_ready_to_diff(pipeline):
            return {
                "message": f"Your pipeline is already created, and are await to diff.",
                "pipeline_stage": pipeline.stage.value,
            }

        raise_message = {
            "message": f"Ocurre an error when try aling your pipeline, await to more iformation.",
            "pipeline_stage": pipeline.stage.value,
        }

        raise Exception(raise_message)

    def _all_genome_files_downloaded(self, pipeline: Pipeline):
        return (
            pipeline.reference_genome.genome_files.fasta == GenomeStatusEnum.DOWNLOADED
            and pipeline.reference_genome.genome_files.gtf
            == GenomeStatusEnum.DOWNLOADED
        )

    def _read_to_generate_genome_index(self, pipeline: Pipeline):
        return (
            self._all_genome_files_downloaded(pipeline)
            and pipeline.reference_genome.genome_files.index == GenomeStatusEnum.PENDING
        )

    def _is_completed_sra_files_by_status(
        self, pipeline: Pipeline, status: SRAFileStatusEnum
    ):

        return (
            pipeline.control_organism.srr_1.status == status
            and pipeline.control_organism.srr_2.status == status
            and pipeline.control_organism.srr_3.status == status
            and pipeline.experiment_organism.srr_1.status == status
            and pipeline.experiment_organism.srr_2.status == status
            and pipeline.experiment_organism.srr_3.status == status
        )

    def _is_ready_to_converter(self, pipeline: Pipeline):
        sra_files_downloaded = self._is_completed_sra_files_by_status(
            pipeline, SRAFileStatusEnum.DOWNLOADED
        )

        if sra_files_downloaded and pipeline.stage == PipelineStageEnum.DOWNLOADED:
            return True

        if sra_files_downloaded and pipeline.stage == PipelineStageEnum.PENDING:
            self.pipeline_repository.update_status(
                pipeline_id=pipeline.id,
                pipeline_stage=PipelineStageEnum.DOWNLOADED,
            )

            return True

        return False

    def _is_ready_to_trim(self, pipeline: Pipeline):
        sra_files_converted = self._is_completed_sra_files_by_status(
            pipeline, SRAFileStatusEnum.CONVERTED
        )

        if sra_files_converted and pipeline.stage == PipelineStageEnum.CONVERTED:
            return True

        if sra_files_converted and pipeline.stage == PipelineStageEnum.DOWNLOADED:
            self.pipeline_repository.update_status(
                pipeline_id=pipeline.id,
                pipeline_stage=PipelineStageEnum.CONVERTED,
            )

            return True

        return False

    def _is_ready_to_aling(self, pipeline: Pipeline):
        sra_files_trimmed = self._is_completed_sra_files_by_status(
            pipeline, SRAFileStatusEnum.TRIMMED
        )

        is_index_genome_generated = (
            pipeline.reference_genome.genome_files.index == GenomeStatusEnum.GENERATED
        )

        files_already_done_to_align = sra_files_trimmed and is_index_genome_generated

        print("files_already_done_to_align", files_already_done_to_align)

        if files_already_done_to_align and pipeline.stage == PipelineStageEnum.TRIMMED:
            return True

        if (
            files_already_done_to_align
            and pipeline.stage == PipelineStageEnum.CONVERTED
        ):
            self.pipeline_repository.update_status(
                pipeline_id=pipeline.id,
                pipeline_stage=PipelineStageEnum.TRIMMED,
            )

            return True

        return False

    def _is_ready_to_count(self, pipeline: Pipeline):
        sra_files_aligned = self._is_completed_sra_files_by_status(
            pipeline, SRAFileStatusEnum.ALIGNED
        )

        gtf_genome_file = (
            pipeline.reference_genome.genome_files.gtf == GenomeStatusEnum.DOWNLOADED
        )

        files_already_done_to_count = sra_files_aligned and gtf_genome_file

        if files_already_done_to_count and pipeline.stage == PipelineStageEnum.ALIGNED:
            return True

        if files_already_done_to_count and pipeline.stage == PipelineStageEnum.TRIMMED:
            self.pipeline_repository.update_status(
                pipeline_id=pipeline.id,
                pipeline_stage=PipelineStageEnum.ALIGNED,
            )

            return True

        return False

    def _is_ready_to_diff(self, pipeline: Pipeline):
        sra_files_counted = self._is_completed_sra_files_by_status(
            pipeline, SRAFileStatusEnum.COUNTED
        )

        de_metadata_file = pipeline.de_metadata_stage == DEMetadataStageEnum.GENERATED

        files_already_done_to_diff = sra_files_counted and de_metadata_file

        if files_already_done_to_diff and pipeline.stage == PipelineStageEnum.COUNTED:
            return True

        if files_already_done_to_diff and pipeline.stage == PipelineStageEnum.ALIGNED:
            self.pipeline_repository.update_status(
                pipeline_id=pipeline.id,
                pipeline_stage=PipelineStageEnum.COUNTED,
            )

            return True

        return False
