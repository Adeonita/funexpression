import os
from ports.infrastructure.storage.storage_path_port import GenomePaths, Paths


class StoragePathsAdapter:

    def get_genome_paths(self, genome_id: str) -> GenomePaths:
        return GenomePaths(
            fasta_path=f"./temp/{genome_id}.fna", gtf_path=f"./temp/{genome_id}.gtf"
        )

    def get_converting_paths(self, pipeline_id, organism_group, sra_id):
        pass

    def get_trimming_paths(self, pipeline_id, organism_group, sra_id) -> Paths:

        self._create_outdir_if_not_exist(
            pipeline_id=pipeline_id, step="TRIMMED", group=organism_group
        )

        return Paths(
            input=f"pipelines/{pipeline_id}/CONVERTED/{organism_group}/{sra_id}/{sra_id}.fastq",
            output=f"pipelines/{pipeline_id}/TRIMMED/{organism_group}/{sra_id}.fq.gz",
        )

    def get_aligner_path(self, pipeline_id: str, organism_group: str, sra_id: str):
        return Paths(
            input=f"pipelines/{pipeline_id}/TRIMMED/{organism_group}/{sra_id}.fq.gz",
            output=f"pipelines/{pipeline_id}/ALIGNER/{organism_group}/{sra_id}.bam",
        )

    def _create_outdir_if_not_exist(self, pipeline_id: str, step: str, group: str):
        temp_files = os.path.join("pipelines/", pipeline_id, step, group)

        if not os.path.exists(temp_files):
            os.makedirs(temp_files)
            return temp_files

        return None
