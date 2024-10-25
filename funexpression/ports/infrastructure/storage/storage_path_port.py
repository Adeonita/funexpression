from typing import Protocol
from dataclasses import dataclass


@dataclass
class Paths:
    input: str
    output: str


class GenomePaths:
    gtf_path: str
    fasta_path: str


class StoragePathsPort(Protocol):

    def get_genome_paths(self, fasta_path: str, gtf_path: str) -> GenomePaths:
        pass

    def get_trimming_paths(self, pipeline_id, organism_group, sra_id) -> Paths:
        pass
