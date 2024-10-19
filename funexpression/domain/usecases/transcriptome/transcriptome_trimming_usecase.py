from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum
from domain.usecases.transcriptome.input.trimming_transcriptome_usecase_input import (
    TrimmingTranscriptomeUseCaseInput,
)
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from ports.infrastructure.storage.storage_path_port import StoragePathsPort
from ports.infrastructure.trimmer.trimmer_port import TrimmerPort


class TranscriptomeTrimming:
    def __init__(
        self,
        trimmer: TrimmerPort,
        storage_paths: StoragePathsPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.trimmer = trimmer
        self.storage_paths = storage_paths
        self.pipeline_repository = pipeline_repository

    def execute(self, input: TrimmingTranscriptomeUseCaseInput) -> None:

        self.trimmer.trim(
            sra_id=input.sra_id,
            trimming_type=input.trimming_type,
            input_path=input.input_path,
            output_path=input.output_path,
        )

        self.pipeline_repository.update_sra_file_status(
            pipeline_id=input.pipeline_id,
            sra_id=input.sra_id,
            status=SRAFileStatusEnum.TRIMMED,
        )

        print("Sending to the alignment queue...")
        # TODO: send to alignment queue
        print("Message sent to the alignment queue!")

        if self.pipeline_repository.is_all_sra_files_trimmed(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id, pipeline_stage=PipelineStageEnum.TRIMMED
            )

            print("Trimming step done!")
