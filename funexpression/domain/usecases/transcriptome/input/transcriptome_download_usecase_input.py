from dataclasses import dataclass


@dataclass
class TranscriptomeDownloadUseCaseInput:
    sra_id: str
    pipeline_id: int
