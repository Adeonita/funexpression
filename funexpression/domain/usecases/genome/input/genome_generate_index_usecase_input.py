from dataclasses import dataclass


@dataclass
class GenomeGenerateIndexUseCaseInput:
    genome_id: str
    pipeline_id: str
    genome_gtf_path: str
    genome_fasta_path: str
