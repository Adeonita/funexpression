from dataclasses import dataclass


@dataclass
class TranscriptomeDifferUseCaseInput:
    pipeline_id: str
    sra_files: dict
