from typing import Protocol


class TaskPort(Protocol):

    def sra_transcriptome_download(sra_id: str, pipeline_id: str):
        pass

    def sra_to_fasta_conversion(sra_id, pipeline_id, organism_group):
        pass
