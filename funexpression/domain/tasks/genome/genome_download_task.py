from domain.entities.pipeline import Pipeline
from infrastructure.celery import download_genome_task


class GenomeDownloadTask:
    def download_genome(self, pipeline: Pipeline):
        download_genome_task(
            genome_id=pipeline.reference_genome.acession_number, pipeline_id=pipeline.id
        )
