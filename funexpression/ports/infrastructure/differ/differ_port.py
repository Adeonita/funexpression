from typing import Protocol


class DifferPort(Protocol):

    def differ(
        self,
        pipeline_id: int,
        sra_files: dict,
        diffed_output_paths: dict,
        p_adj: float,
        log2_fc_threshold: float,
    ) -> None:
        pass
