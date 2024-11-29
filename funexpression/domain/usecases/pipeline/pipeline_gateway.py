from domain.entities.de_metadata import DEMetadataStageEnum
from domain.entities.genome import GenomeStatusEnum
from domain.entities.pipeline import Pipeline
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum
from domain.tasks.pipeline_task import PipelineTask
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)


class PipelineGateway:

    def __init__(
        self, pipeline_repository: PipelineRepositoryPort, pipeline_task: PipelineTask
    ):
        self.pipeline_repository = pipeline_repository
        self.pipeline_task = pipeline_task

    def start(self, pipeline: Pipeline):
        self.pipeline_task.start(pipeline=pipeline)

    def handle(self, pipeline: Pipeline):
        if self._is_ready_to_download(pipeline):
            return {
                "message": f"Your pipeline is already created, and the sra files are awaiting was sent to downloading",
                "pipeline_stage": pipeline.stage.value,
            }

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

        if self._is_done(pipeline):
            return {
                "message": f"Your pipeline is already done, await the result in your email.",
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

    def _is_ready_to_download(self, pipeline: Pipeline):
        sra_files_pending = self._is_completed_sra_files_by_status(
            pipeline, SRAFileStatusEnum.PENDING
        )

        if pipeline.stage == PipelineStageEnum.PENDING:
            return True

    def _is_ready_to_converter(self, pipeline: Pipeline):
        sra_files_downloaded = self._is_completed_sra_files_by_status(
            pipeline, SRAFileStatusEnum.DOWNLOADED
        )

        if sra_files_downloaded and pipeline.stage == PipelineStageEnum.DOWNLOADED:
            self.pipeline_task.convert_transcripomes(pipeline=pipeline)
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
            self.pipeline_task.trimming_transcriptomes(pipeline)
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

        if files_already_done_to_align and pipeline.stage == PipelineStageEnum.TRIMMED:
            self.pipeline_task.aling_transcriptomes(pipeline)

            return True

        if (
            files_already_done_to_align
            and pipeline.stage == PipelineStageEnum.CONVERTED
        ):
            self.pipeline_task.aling_transcriptomes(pipeline)

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

        files_already_done_to_diff = sra_files_counted

        if files_already_done_to_diff and pipeline.stage == PipelineStageEnum.COUNTED:
            return True

        if files_already_done_to_diff and pipeline.stage == PipelineStageEnum.ALIGNED:
            self.pipeline_repository.update_status(
                pipeline_id=pipeline.id,
                pipeline_stage=PipelineStageEnum.COUNTED,
            )

            return True

        return False

    def _is_done(self, pipeline: Pipeline):
        sra_files_diffed = self._is_completed_sra_files_by_status(
            pipeline, SRAFileStatusEnum.DIFFED
        )

        files_already_done = sra_files_diffed

        if files_already_done and pipeline.stage == PipelineStageEnum.DIFFED:
            return True

        if files_already_done and pipeline.stage == PipelineStageEnum.COUNTED:
            self.pipeline_repository.update_status(
                pipeline_id=pipeline.id,
                pipeline_stage=PipelineStageEnum.DIFFED,
            )

            return True

        return False
