from dataclasses import dataclass


@dataclass
class GenomeAlignerUseCaseInput:
    pipeline_id: str
    sra_id: str
    # genome_id: str TODO: add genome_id
    organism_group: str
    genome_index_path: str
    trimed_transcriptome_path: str
    aligned_transcriptome_path: str
