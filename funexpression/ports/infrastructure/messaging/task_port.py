from typing import Protocol


class TaskPort(Protocol):

    def sra_transcriptome_download(self, sra_id: str, pipeline_id: str):
        pass

    def sra_to_fasta_conversion(self, pipeline_id: str):
        pass
