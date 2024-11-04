from dataclasses import dataclass


@dataclass
class TranscriptomeCountUseCaseInput:
    pipeline_id: str
    sra_id: str
    organism_group: str
    aligned_transcriptome_path: str
    gtf_genome_file_path: str
    counted_transcriptome_path: str
