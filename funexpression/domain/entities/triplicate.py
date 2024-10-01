from enum import Enum
from dataclasses import dataclass


class SRAFileStatusEnum(Enum):
    PENDING = "PENDING"
    DOWNLOADING = "DOWNLOADING"
    OK = "OK"


@dataclass
class SRAFile:
    acession_number: str
    status: SRAFileStatusEnum


@dataclass
class Triplicate:
    srr_1: SRAFile
    srr_2: SRAFile
    srr_3: SRAFile
