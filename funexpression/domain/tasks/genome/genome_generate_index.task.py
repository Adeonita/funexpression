from domain.entities.pipeline import Pipeline
from infrastructure.celery import generate_index_genome_task


class GenomeGenerateIndexTask:
    def _generate_genome_index(self, pipeline: Pipeline):
        paths = self.storage_paths.get_genome_paths(
            pipeline.reference_genome.acession_number
        )

        generate_index_genome_task(
            pipeline_id=pipeline.id,
            genome_id=pipeline.reference_genome.acession_number,
            gtf_genome_path=paths.gtf_path,
            fasta_genome_path=paths.fasta_path,
            index_genome_output_path=paths.index_path,
        )