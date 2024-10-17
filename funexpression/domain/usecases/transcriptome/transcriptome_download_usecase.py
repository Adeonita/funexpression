from domain.usecases.base_usecase import BaseUseCase
from domain.entities.triplicate import SRAFileStatusEnum
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from ports.infrastructure.bio_database.geo_adapter_port import GeoAdapterPort
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)

from infrastructure.celery import convert_sra_to_fasta_task


class TranscriptomeDownloadUseCase(BaseUseCase):

    def __init__(
        self,
        geo_adapter: GeoAdapterPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.geo_adapter = geo_adapter
        self.pipeline_repository = pipeline_repository

    def execute(self, input: TranscriptomeDownloadUseCaseInput) -> str:
        sra_id = input.sra_id
        pipeline_id = input.pipeline_id
        organism_group = input.organism_group

        print(f"Processing download for {sra_id}")

        sra_path = self.geo_adapter.get_sra_sequence_from_ncbi(input.sra_id)
        self.pipeline_repository.update_sra_file_status(
            pipeline_id=input.pipeline_id,
            sra_id=input.sra_id,
            STATUS=SRAFileStatusEnum.DOWNLOADED,
        )

        if self.pipeline_repository.is_all_file_download_downloaded(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id,
                pipeline_stage=PipelineStageEnum.DOWNLOADED,
            )
            print("Download step done")

            print("Sending to the conversion queue...")

            convert_sra_to_fasta_task(sra_id, pipeline_id, organism_group)

            print("Message sent to the conversion queue!")

        return sra_path
