from dataclasses import dataclass

from domain.entities.triplicate import OrganinsGroupEnum


@dataclass
class TranscriptomeDownloadUseCaseInput:
    sra_id: str
    pipeline_id: str
    organism_group: OrganinsGroupEnum
