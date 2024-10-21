from dataclasses import dataclass


@dataclass
class GenomeDownloadUseCaseInput:
    genome_id: str
    pipeline_id: str
