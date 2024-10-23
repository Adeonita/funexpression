from typing import Protocol


class GenBankPort(Protocol):

    def get_fasta_genome_from_ncbi(self, genome_id: str) -> str:
        pass

    def get_gtf_genome_from_ncbi(self, genome_id: str) -> str:
        pass

    def get_gtf_and_fasta_genome_from_ncbi(self, genome_id: str):
        pass
