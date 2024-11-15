from typing import Protocol
from dataclasses import dataclass


@dataclass
class Paths:
    input: str
    output: str


@dataclass
class GenomePaths:
    gtf_path: str
    fasta_path: str
    index_path: str


class StoragePathsPort(Protocol):

    def get_genome_paths(self, genome_id) -> GenomePaths:
        pass

    def get_converting_paths(self, pipeline_id, organism_group, sra_id) -> Paths:
        pass

    def get_trimming_paths(self, pipeline_id, organism_group, sra_id) -> Paths:
        pass

    def get_aligner_path(
        self, pipeline_id: str, organism_group: str, sra_id: str
    ) -> Paths:
        pass

    def get_counting_path(
        self, pipeline_id: str, organism_group: str, sra_id: str
    ) -> Paths:
        pass

    def get_to_diffing_path(self, sra_files: dict, pipeline_id: str):
        pass

    def _create_outdir_if_not_exist(
        self, pipeline_id: str, step: str, group: str, sra_id=None
    ):
        pass

    def create_pipeline_directory_structure(pipeline_id: str):
        pass
