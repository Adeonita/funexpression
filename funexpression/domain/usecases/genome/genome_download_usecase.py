from domain.usecases.base_usecase import BaseUseCase
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.genome import GenomeFilesEnum, GenomeStatusEnum
from ports.infrastructure.bio_database.genbank_port import GenBankPort

from domain.usecases.genome.input.genome_downlaod_usecase_input import (
    GenomeDownloadUseCaseInput,
)
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)


class GenomeDownloadUseCase(BaseUseCase):

    def __init__(
        self,
        genbank_adapter: GenBankPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.genbank_adapter = genbank_adapter
        self.pipeline_repository = pipeline_repository

    def execute(self, input: GenomeDownloadUseCaseInput) -> str:
        genome_id = input.genome_id
        pipeline_id = input.pipeline_id

        print(f"Processing download for {genome_id}")

        gft_genome = self.genbank_adapter.get_gft_genome_from_ncbi(genome_id=genome_id)
        fasta_genome = self.genbank_adapter.get_fasta_genome_from_ncbi(
            genome_id=genome_id
        )
        is_read_genomes_files = gft_genome and fasta_genome

        if gft_genome:
            self.pipeline_repository.update_genome_file_status(
                pipeline_id=pipeline_id,
                genome_id=genome_id,
                file_status=GenomeStatusEnum.DOWNLOADED,
                file=GenomeFilesEnum.GFT,
            )

        if fasta_genome:
            self.pipeline_repository.update_genome_file_status(
                pipeline_id=pipeline_id,
                genome_id=genome_id,
                file_status=GenomeStatusEnum.DOWNLOADED,
                file=GenomeFilesEnum.FASTA,
            )

        if is_read_genomes_files:
            self.pipeline_repository.update_genome_reference_status(
                pipeline_id=pipeline_id,
                genome_id=genome_id,
                status=GenomeStatusEnum.DOWNLOADED,
            )

        if self.pipeline_repository.is_all_file_download_downloaded(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id,
                pipeline_stage=PipelineStageEnum.DOWNLOADED,
            )
            print("Download step done")

            print("Sending to the conversion queue...")

            # convert_sra_to_fasta_task(sra_id, pipeline_id, organism_group)

            print("Message sent to the conversion queue!")
