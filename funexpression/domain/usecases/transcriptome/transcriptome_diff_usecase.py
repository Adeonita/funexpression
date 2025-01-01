from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum

from domain.usecases.transcriptome.input.differ_transcriptome_usecase_input import (
    TranscriptomeDifferUseCaseInput,
)
from infrastructure.reports.email_sender import EmailSender
from ports.infrastructure.differ.differ_port import DifferPort
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from ports.infrastructure.storage.storage_path_port import StoragePathsPort


class TranscriptomeDiffUseCase:
    def __init__(
        self,
        diff: DifferPort,
        email_sender: EmailSender,
        storage_paths: StoragePathsPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.diff_port = diff
        self.email_sender = email_sender
        self.storage_paths = storage_paths
        self.pipeline_repository = pipeline_repository

    def execute(self, input: TranscriptomeDifferUseCaseInput):
        diffed_output = self.storage_paths.get_diffed_file_paths(input.pipeline_id)

        p_adj = self.pipeline_repository.get_p_adj_by_pipeline(input.pipeline_id)
        log2_fc_threshold = (
            self.pipeline_repository.get_log_2_fold_change_threshold_by_pipeline(
                input.pipeline_id
            )
        )

        self.diff_port.differ(
            pipeline_id=input.pipeline_id,
            sra_files=input.sra_files,
            diffed_output_paths=diffed_output,
            p_adj=p_adj,
            log2_fc_threshold=log2_fc_threshold,
        )

        sra_files = self.pipeline_repository.get_sra_files(input.pipeline_id)

        for sra in sra_files:
            sra_id = sra[0]
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

        pipeline_info = self.pipeline_repository.get_pipeline_info(input.pipeline_id)

        self.email_sender.send_email_with_results(pipeline_info, diffed_output)

        self.storage_paths.remove_trash(input.pipeline_id)

        return
