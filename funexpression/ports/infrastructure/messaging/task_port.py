from typing import Protocol, Callable


class TaskPort(Protocol):

    def sra_transcriptome_download(self, sra_id: str, pipeline_id: str):
        pass
