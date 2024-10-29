from typing import Protocol


class AlignerPort(Protocol):

    def generate_genome_index(
        self,
        gtf_genome_path: str,
        fasta_genome_path: str,
        index_genome_output_path: str,
    ) -> str:
        pass

    def align(
        self,
        sra_id: str,
        genome_index_path: str,
        genome_fasta_path: str,
        input_path: str,
        output_path: str,
    ) -> None:
        pass
