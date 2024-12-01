import os
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import OrganinsGroupEnum
from domain.factories.genome_aligner_usecase_factory import GenomeAlignerUseCaseFactory
from domain.factories.genome_download_usecase_factory import (
    GenomeDownloadUseCaseFactory,
)
from domain.factories.genome_generate_index_usecase_factory import (
    GenomeIndexGenerateUseCaseFactory,
)
from domain.factories.transcriptome.conversion_sra_to_fasta_usecase_factory import (
    ConversionSraToFastaUseCaseFactory,
)
from domain.factories.transcriptome.transcriptome_counting_usecase_factory import (
    TranscriptomeCountingUseCaseFactory,
)
from domain.factories.transcriptome.transcriptome_diffing_use_case_factory import (
    DifferTranscriptomeUseCaseFactory,
)
from domain.factories.transcriptome.transcriptome_download_usecase_factory import (
    TranscriptomeDownloadUseCaseFactory,
)
from domain.factories.transcriptome.transcriptome_trimming_usecase_factory import (
    TranscriptomeTrimmingUseCaseFactory,
)
from domain.usecases.genome.input.genome_aligner_usecase_input import (
    GenomeAlignerUseCaseInput,
)
from domain.usecases.genome.input.genome_downlaod_usecase_input import (
    GenomeDownloadUseCaseInput,
)
from domain.usecases.genome.input.genome_generate_index_usecase_input import (
    GenomeGenerateIndexUseCaseInput,
)
from domain.usecases.transcriptome.input.conversion_sra_to_fasta_usecase_input import (
    ConversionSraToFastaUseCaseInput,
)
from domain.usecases.transcriptome.input.counting_transcriptome_usecase import (
    TranscriptomeCountUseCaseInput,
)
from domain.usecases.transcriptome.input.differ_transcriptome_usecase_input import (
    TranscriptomeDifferUseCaseInput,
)
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)
from domain.usecases.transcriptome.input.trimming_transcriptome_usecase_input import (
    TrimmingTranscriptomeUseCaseInput,
    TrimmingTypeEnum,
)
from infrastructure.celery import app
from infrastructure.logger.logger import log_processing_queue_error_message
from infrastructure.messaging.task_helper import set_pipeline_status_to_failed
from ports.infrastructure.messaging.task_port import TaskPort

MAX_RETRYES = int(os.getenv("TASK_MAX_RETRIES"))


class Task(TaskPort):

    @app.task(
        bind=True,
        queue="geo_sra_download",
        max_retries=MAX_RETRYES,
    )
    def sra_transcriptome_download(
        self, sra_id: str, pipeline_id: str, organism_group: str
    ):
        try:
            transcriptome_download_usecase = (
                TranscriptomeDownloadUseCaseFactory.create()
            )

            input = TranscriptomeDownloadUseCaseInput(
                sra_id=sra_id, pipeline_id=pipeline_id, organism_group=organism_group
            )
            transcriptome_download_usecase.execute(input)
        except Exception as e:
            if self.request.retries >= MAX_RETRYES:
                set_pipeline_status_to_failed(pipeline_id)

            log_processing_queue_error_message(sra_id, "download", e)
            self.retry(exc=e)

    @app.task(bind=True, queue="genbank_ncbi_download", max_retries=MAX_RETRYES)
    def genome_download(self, genome_id: str, pipeline_id: str):
        try:
            genome_download_usecase = GenomeDownloadUseCaseFactory.create()
            input = GenomeDownloadUseCaseInput(
                genome_id=genome_id, pipeline_id=pipeline_id
            )
            genome_download_usecase.execute(input)
        except Exception as e:
            if self.request.retries >= MAX_RETRYES:
                set_pipeline_status_to_failed(pipeline_id)

            log_processing_queue_error_message(genome_id, "download genome", e)
            raise self.retry(exc=e)

    @app.task(bind=True, queue="sra_to_fasta_conversion", max_retries=MAX_RETRYES)
    def sra_to_fasta_conversion(self, sra_id, pipeline_id, organism_group):
        try:
            conversion_usecase = ConversionSraToFastaUseCaseFactory.create()
            conversion_usecase.execute(sra_id, pipeline_id, organism_group)
        except Exception as e:
            if self.request.retries >= MAX_RETRYES:
                set_pipeline_status_to_failed(pipeline_id)

            log_processing_queue_error_message(sra_id, "download genome", e)
            raise self.retry(exc=e)

    @app.task(bind=True, queue="trimming_transcriptome", max_retries=MAX_RETRYES)
    def trimming_transcriptome(
        self,
        pipeline_id: str,
        sra_id: str,
        organism_group: str,
        trimming_type: TrimmingTypeEnum,
        input_path: str,
        output_path: str,
    ):
        try:
            input = TrimmingTranscriptomeUseCaseInput(
                pipeline_id=pipeline_id,
                sra_id=sra_id,
                organism_group=organism_group,
                trimming_type=trimming_type,
                input_path=input_path,
                output_path=output_path,
            )
            trimming_usecase = TranscriptomeTrimmingUseCaseFactory.create()
            trimming_usecase.execute(input)
        except Exception as e:
            if self.request.retries >= MAX_RETRYES:
                set_pipeline_status_to_failed(pipeline_id)

            log_processing_queue_error_message(sra_id, "trimming", e)
            raise self.retry(exc=e)

    @app.task(bind=True, queue="generate_index_genome", max_retries=MAX_RETRYES)
    def generate_index_genome(
        self,
        pipeline_id: str,
        genome_id: str,
        gtf_genome_path: str,
        fasta_genome_path: str,
        index_genome_output_path: str,
    ):
        try:
            input = GenomeGenerateIndexUseCaseInput(
                pipeline_id=pipeline_id,
                genome_id=genome_id,
                gtf_genome_path=gtf_genome_path,
                fasta_genome_path=fasta_genome_path,
                index_genome_output_path=index_genome_output_path,
            )

            genome_index_generate_usecase = GenomeIndexGenerateUseCaseFactory.create()

            genome_index_generate_usecase.execute(input)
        except Exception as e:
            if self.request.retries >= MAX_RETRYES:
                set_pipeline_status_to_failed(pipeline_id)

            log_processing_queue_error_message(genome_id, "downloading genome", e)
            raise self.retry(exc=e)

    @app.task(bind=True, queue="aligner_transcriptome", max_retries=MAX_RETRYES)
    def aligner_transcriptome(
        self,
        pipeline_id: str,
        sra_id: str,
        organism_group: OrganinsGroupEnum,
        genome_index_path: str,
        transcriptome_trimed_path: str,
        aligned_transcriptome_path: str,
    ):

        try:
            input = GenomeAlignerUseCaseInput(
                pipeline_id=pipeline_id,
                sra_id=sra_id,
                organism_group=organism_group,
                genome_index_path=genome_index_path,
                trimed_transcriptome_path=transcriptome_trimed_path,
                aligned_transcriptome_path=aligned_transcriptome_path,
            )

            genome_aligner_usecase = GenomeAlignerUseCaseFactory.create()
            genome_aligner_usecase.execute(input)
        except Exception as e:
            if self.request.retries >= MAX_RETRYES:
                set_pipeline_status_to_failed(pipeline_id)

            log_processing_queue_error_message(sra_id, "align transcriptome", e)
            raise self.retry(exc=e)

    @app.task(bind=True, queue="counter_transcriptome", max_retries=MAX_RETRYES)
    def counter_transcriptome(
        self,
        pipeline_id: str,
        sra_id: str,
        organism_group: OrganinsGroupEnum,
        aligned_transcriptome_path: str,
        gtf_genome_file_path: str,
        counted_transcriptome_path: str,
    ):
        try:
            input = TranscriptomeCountUseCaseInput(
                pipeline_id=pipeline_id,
                sra_id=sra_id,
                organism_group=organism_group,
                aligned_transcriptome_path=aligned_transcriptome_path,
                gtf_genome_file_path=gtf_genome_file_path,
                counted_transcriptome_path=counted_transcriptome_path,
            )

            transcriptome_count_usecase = TranscriptomeCountingUseCaseFactory.create()
            transcriptome_count_usecase.execute(input)
        except Exception as e:
            if self.request.retries >= MAX_RETRYES:
                set_pipeline_status_to_failed(pipeline_id)

            log_processing_queue_error_message(sra_id, "count transcriptome", e)
            raise self.retry(exc=e)

    @app.task(
        bind=True, queue="generate_diferential_expression", max_retries=MAX_RETRYES
    )
    def generate_diferential_expression(self, pipeline_id, sra_files):
        try:
            input = TranscriptomeDifferUseCaseInput(
                pipeline_id=pipeline_id,
                sra_files=sra_files,
            )

            transcriptome_differ_usecase = DifferTranscriptomeUseCaseFactory.create()
            transcriptome_differ_usecase.execute(input)
        except Exception as e:
            if self.request.retries >= MAX_RETRYES:
                set_pipeline_status_to_failed(pipeline_id)

            log_processing_queue_error_message(pipeline_id, "differ transcriptome", e)
            raise self.retry(exc=e)
