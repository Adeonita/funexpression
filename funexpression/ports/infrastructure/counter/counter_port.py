from typing import Protocol


class CounterPort(Protocol):

    def count(
        self,
        aligned_file_path: str,
        gtf_genome_file_path: str,
        counted_file_path: str,
        sra_id: str,
    ) -> str:
        pass
