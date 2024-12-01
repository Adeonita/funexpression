from enum import Enum


class PipelineStageEnum(Enum):
    PENDING = "PENDING"
    DOWNLOADED = "DOWNLOADED"
    CONVERTED = "CONVERTED"
    TRIMMED = "TRIMMED"
    ALIGNED = "ALIGNED"
    COUNTED = "COUNTED"
    DIFFED = "DIFFED"
    DONE = "DONE"
    FAILED = "FAILED"
