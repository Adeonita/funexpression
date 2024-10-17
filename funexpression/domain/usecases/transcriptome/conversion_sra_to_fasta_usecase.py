import os
from domain.entities.triplicate import SRAFileStatusEnum
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from infrastructure.sra_tools.fasterq_dump_adapter import FasterqDumpAdapter
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)


class ConversionSraToFastaUseCase:
    def __init__(
        self,
        fasterq_dump_adapter: FasterqDumpAdapter,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.pipeline_repository = pipeline_repository
        self.fasterq_dump_adapter = fasterq_dump_adapter

    def execute(self, sra_id, pipeline_id, organism_group):

        output_dir = self._create_outdir_if_not_exist(
            pipeline_id, "CONVERTED", organism_group, sra_id
        )

        self.fasterq_dump_adapter.dump_sra_to_fasta(sra_id, output_dir)

        self.pipeline_repository.update_sra_file_status(
            pipeline_id=pipeline_id,
            sra_id=sra_id,
            status=SRAFileStatusEnum.CONVERTED,
        )

        if self.pipeline_repository.is_all_file_download_converted(pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=pipeline_id,
                pipeline_stage=PipelineStageEnum.CONVERTED,
            )
            print("Converted step done")

            print("Sending to the trimming queue...")

            trimming_input = {
                "pipeline_id": pipeline_id,
                "organism_group": organism_group,
                "trimming_type": "SE",
                "input_path": f"pipelines/{pipeline_id}/CONVERTED/{organism_group}{sra_id}/{sra_id}.fastq",
                "output_path": f"pipelines/{pipeline_id}/TRIMMED/{organism_group}/{sra_id}.fq.gz",
                #  pipelines/670c3064f3fcd22056f49445/CONTROL/SRR10042980/SRR10042980.fastq
            }

            # TODO: Implement trimming task
            # convert_sra_to_fasta_task(sra_id, pipeline_id, organism_group)

            print("Message sent to the trimming queue!")

    def _create_outdir_if_not_exist(
        self, pipeline_id: str, step: str, group: str, acession_number: str
    ):
        temp_files = os.path.join(
            "pipelines/", pipeline_id, step, group, acession_number
        )

        if not os.path.exists(temp_files):
            os.makedirs(temp_files)
            return temp_files

        return None
