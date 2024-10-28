from typing import Protocol


class AlignerPort(Protocol):
    def align(
        self,
        sra_id: str,
        genome_index_path: str,
        genome_fasta_path: str,
        input_path: str,
        output_path: str,
    ) -> None:
        pass
