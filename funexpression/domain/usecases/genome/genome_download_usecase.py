from domain.usecases.base_usecase import BaseUseCase
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.genome import GenomeFilesEnum, GenomeStatusEnum
from domain.usecases.helpers.helpers import send_sra_to_conversion_queue_in_bulk
from infrastructure.celery import generate_index_genome_task
from ports.infrastructure.bio_database.genbank_port import GenBankPort

from domain.usecases.genome.input.genome_downlaod_usecase_input import (
    GenomeDownloadUseCaseInput,
)
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)
from ports.infrastructure.storage.storage_path_port import StoragePathsPort


class GenomeDownloadUseCase(BaseUseCase):

    def __init__(
        self,
        genbank_adapter: GenBankPort,
        storage_paths: StoragePathsPort,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.storage_paths = storage_paths
        self.genbank_adapter = genbank_adapter
        self.pipeline_repository = pipeline_repository

    def execute(self, input: GenomeDownloadUseCaseInput) -> str:
        genome_id = input.genome_id
        pipeline_id = input.pipeline_id

        print(f"Processing download for {genome_id}")

        # TODO: descomentar após os testes
        # downloaded = self.genbank_adapter.get_gtf_and_fasta_genome_from_ncbi(genome_id)

        # TODO: remover após os testes e manter o uso do storage paths
        # downloaded = {
        #     "gtf_path": f"./temp_files/{genome_id}.gtf",
        #     "fasta_path": f"./temp_files/{genome_id}.fasta",
        # }

        # gtf_genome = downloaded.get("gtf_path")
        # fasta_genome = downloaded.get("fasta_path")

        genome_paths = self.storage_paths.get_genome_paths(genome_id)

        gtf_genome = genome_paths.gtf_path
        fasta_genome = genome_paths.fasta_path
        index_genome = genome_paths.index_path

        is_read_genomes_files = gtf_genome and fasta_genome

        if gtf_genome:
            self.pipeline_repository.update_genome_file_status(
                pipeline_id=pipeline_id,
                genome_id=genome_id,
                file_status=GenomeStatusEnum.DOWNLOADED,
                file=GenomeFilesEnum.GTF,
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

            generate_index_genome_task(
                pipeline_id=pipeline_id,
                genome_id=genome_id,
                gtf_genome_path=gtf_genome,
                fasta_genome_path=fasta_genome,
                index_genome_output_path=index_genome,
            )

        if self.pipeline_repository.is_all_file_download_downloaded(input.pipeline_id):
            self.pipeline_repository.update_status(
                pipeline_id=input.pipeline_id,
                pipeline_stage=PipelineStageEnum.DOWNLOADED,
            )
            print("Download step done")

            print("Sending to the conversion queue...")

            sra_files = self.pipeline_repository.get_sra_files(input.pipeline_id)

            send_sra_to_conversion_queue_in_bulk(sra_files, pipeline_id)

            print("Message sent to the conversion queue!")
