from enum import StrEnum
from dataclasses import dataclass


class GenomeStatusEnum(StrEnum):
    PENDING = "PENDING"
    DOWNLOADED = "DOWNLOADED"


class GenomeFilesEnum(StrEnum):
    GFT = "GFT"
    FASTA = "FASTA"


@dataclass
class GenomeFiles:
    gft: GenomeStatusEnum
    fasta: GenomeStatusEnum


@dataclass
class Genome:
    acession_number: str
    state: GenomeStatusEnum
    genome_files: GenomeFiles
