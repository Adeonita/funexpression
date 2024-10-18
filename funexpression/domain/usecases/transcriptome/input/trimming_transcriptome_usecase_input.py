from dataclasses import dataclass
from enum import StrEnum


class TrimmingTypeEnum(StrEnum):
    SINGLE_END = "SINGLE_END"
    PAIRED_END = "PAIRED_END"


@dataclass
class TrimmingTranscriptomeUseCaseInput:
    pipeline_id: str
    sra_id: str
    organism_group: str
    trimming_type: TrimmingTypeEnum
    input_path: str
    output_path: str
