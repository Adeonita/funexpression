from typing import Protocol


class TaskPort(Protocol):

    def sra_transcriptome_download(sra_id: str, pipeline_id: str, organism_group: str):
        pass

    def sra_to_fasta_conversion(sra_id: str, pipeline_id: str, organism_group: str):
        pass
