from typing import Protocol


class DifferPort(Protocol):

    def differ(
        self, pipeline_id: str, sra_files: dict, diffed_output_paths: dict
    ) -> None:
        pass
