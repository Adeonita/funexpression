from dataclasses import dataclass


@dataclass
class GenomeGenerateIndexUseCaseInput:
    pipeline_id: str
    genome_id: str
    gtf_genome_path: str
    fasta_genome_path: str
    index_genome_output_path: str
