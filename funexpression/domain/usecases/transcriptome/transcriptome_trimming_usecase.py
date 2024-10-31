from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFileStatusEnum
from domain.usecases.transcriptome.input.trimming_transcriptome_usecase_input import (
    TrimmingTranscriptomeUseCaseInput,
)
from infrastructure.celery import aligner_transcriptome_task
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

        genome_id = self.pipeline_repository.get_genome_id_by_pipeline(
            input.pipeline_id
        )
        genome_paths = self.storage_paths.get_genome_paths(genome_id)
        aligner_paths = self.storage_paths.get_aligner_path(
            input.pipeline_id, input.organism_group, input.sra_id
        )
        aligner_transcriptome_task(
            pipeline_id=input.pipeline_id,
            sra_id=input.sra_id,
            organism_group=input.organism_group,
            genome_index_path=genome_paths.gtf_path,
            trimed_transcriptome_path=input.output_path,
            aligned_transcriptome_path=aligner_paths.output,
        )
        print("Message sent to the alignment queue!")

        if self.pipeline_repository.is_all_sra_files_trimmed(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id, pipeline_stage=PipelineStageEnum.TRIMMED
            )

            print("Trimming step done!")
