from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum
from domain.usecases.transcriptome.input.counting_transcriptome_usecase import (
    TranscriptomeCountUseCaseInput,
)
from domain.usecases.transcriptome.input.differ_transcriptome_usecase_input import (
    TranscriptomeDifferUseCaseInput,
)
from infrastructure.celery import diffed_transcriptome_task
from ports.infrastructure.counter.counter_port import CounterPort
from ports.infrastructure.differ.differ_port import DifferPort
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from ports.infrastructure.storage.storage_path_port import StoragePathsPort


class TranscriptomeDiffUseCase:
    def __init__(
        self,
        diff: DifferPort,
        storage_paths: StoragePathsPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.diff_port = diff
        self.storage_paths = storage_paths
        self.pipeline_repository = pipeline_repository

    def execute(self, input: TranscriptomeDifferUseCaseInput):
        diffed_output = self.storage_paths.get_diffed_file_paths(input.pipeline_id)

        self.diff_port.differ(
            pipeline_id=input.pipeline_id,
            sra_files=input.sra_files,
            diffed_output_paths=diffed_output,
        )

        sra_files = self.pipeline_repository.get_sra_files(input.pipeline_id)

        for sra_id in sra_files:

            self.pipeline_repository.update_sra_file_status(
                pipeline_id=input.pipeline_id,
                sra_id=sra_id,
                status=SRAFileStatusEnum.DIFFED,
            )

        if self.pipeline_repository.is_all_sra_files_diffed(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id,
                pipeline_stage=PipelineStageEnum.DIFFED,
            )

            print("Diffed step done!")

            # TODO: Trigger task to send email

        return
