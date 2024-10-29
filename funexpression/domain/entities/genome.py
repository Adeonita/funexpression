from enum import StrEnum
from dataclasses import dataclass


class GenomeStatusEnum(StrEnum):
    PENDING = "PENDING"
    DOWNLOADED = "DOWNLOADED"
    GENERATED = "GENERATED"


class GenomeFilesEnum(StrEnum):
    GTF = "GTF"
    FASTA = "FASTA"
    INDEX = "INDEX"


@dataclass
class GenomeFiles:
    gtf: GenomeStatusEnum
    fasta: GenomeStatusEnum
    index: GenomeStatusEnum


@dataclass
class Genome:
    acession_number: str
    state: GenomeStatusEnum
    genome_files: GenomeFiles
