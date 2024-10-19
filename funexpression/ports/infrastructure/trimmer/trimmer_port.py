from typing import Protocol


class TrimmerPort(Protocol):
    def trim(
        self, sra_id: str, trimming_type: str, input_path: str, output_path: str
    ) -> None:
        pass
