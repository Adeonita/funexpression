from enum import StrEnum
from dataclasses import dataclass


class SRAFileStatusEnum(StrEnum):
    PENDING = "PENDING"
    DOWNLOADED = "DOWNLOADED"
    CONVERTED = "CONVERTED"
    TRIMMED = "TRIMMED"


class OrganinsGroupEnum(StrEnum):
    CONTROL = "CONTROL"
    EXPERIMENT = "EXPERIMENT"


@dataclass
class SRAFile:
    acession_number: str
    status: SRAFileStatusEnum


@dataclass
class Triplicate:
    srr_1: SRAFile
    srr_2: SRAFile
    srr_3: SRAFile
