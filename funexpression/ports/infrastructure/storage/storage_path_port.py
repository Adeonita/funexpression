from typing import Protocol
from dataclasses import dataclass


@dataclass
class Paths:
    input: str
    output: str


class StoragePathsPort(Protocol):

    def get_trimming_paths(self, pipeline_id, organism_group, sra_id) -> Paths:
        pass
