from enum import StrEnum
from dataclasses import dataclass


class GenomeStatusEnum(StrEnum):
    PENDING = "PENDING"
    DOWNLOADED = "DOWNLOADED"


class GenomeFilesEnum(StrEnum):
    GTF = "GTF"
    FASTA = "FASTA"


@dataclass
class GenomeFiles:
    gtf: GenomeStatusEnum
    fasta: GenomeStatusEnum


@dataclass
class Genome:
    acession_number: str
    state: GenomeStatusEnum
    genome_files: GenomeFiles
