from typing import Protocol


class GenBankPort(Protocol):

    def get_fasta_genome_from_ncbi(self, genome_id: str) -> str:
        pass

    def get_gft_genome_from_ncbi(self, genome_id: str) -> str:
        pass
