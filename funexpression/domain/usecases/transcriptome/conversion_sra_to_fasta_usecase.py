import os
from domain.entities.triplicate import SRAFileStatusEnum
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from infrastructure.celery import trimming_transcriptome_task
from infrastructure.sra_tools.fasterq_dump_adapter import FasterqDumpAdapter
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from ports.infrastructure.storage.storage_path_port import StoragePathsPort


class ConversionSraToFastaUseCase:
    def __init__(
        self,
        fasterq_dump_adapter: FasterqDumpAdapter,
        storage_paths: StoragePathsPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.pipeline_repository = pipeline_repository
        self.fasterq_dump_adapter = fasterq_dump_adapter
        self.storage_paths = storage_paths

    def execute(self, sra_id, pipeline_id, organism_group):

        paths = self.storage_paths.get_converting_paths(
            pipeline_id=pipeline_id, organism_group=organism_group, sra_id=sra_id
        )
        output_dir = paths.output

        if output_dir is not None:
            self.fasterq_dump_adapter.dump_sra_to_fasta(sra_id, output_dir)

            self.pipeline_repository.update_sra_file_status(
                pipeline_id=pipeline_id,
                sra_id=sra_id,
                status=SRAFileStatusEnum.CONVERTED,
            )

            print("Sending to the trimming queue...")

            paths = self.storage_paths.get_trimming_paths(
                pipeline_id, organism_group, sra_id
            )

            trimming_transcriptome_task(
                pipeline_id=pipeline_id,
                sra_id=sra_id,
                organism_group=organism_group,
                trimming_type="SE",
                input_path=paths.input,
                output_path=paths.output,
            )

            print("Message sent to the trimming queue!")

            if self.pipeline_repository.is_all_file_download_converted(pipeline_id):
                self.pipeline_repository.update_status(
                    pipeline_id=pipeline_id,
                    pipeline_stage=PipelineStageEnum.CONVERTED,
                )
                print("Converted step done!")
