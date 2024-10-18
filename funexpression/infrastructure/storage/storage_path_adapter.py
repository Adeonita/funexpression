from ports.infrastructure.storage.storage_path_port import Paths


class StoragePathsAdapter:
    def get_converting_paths(self, pipeline_id, organism_group, sra_id):
        pass

    def get_trimming_paths(self, pipeline_id, organism_group, sra_id) -> Paths:

        return Paths(
            input=f"pipelines/{pipeline_id}/CONVERTED/{organism_group}{sra_id}/{sra_id}.fastq",
            output=f"pipelines/{pipeline_id}/TRIMMED/{organism_group}/{sra_id}.fq.gz",
        )
