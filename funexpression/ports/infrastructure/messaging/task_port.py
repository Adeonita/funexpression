from typing import Protocol

from domain.usecases.transcriptome.input.trimming_transcriptome_usecase_input import (
    TrimmingTypeEnum,
)


class TaskPort(Protocol):

    def sra_transcriptome_download(sra_id: str, pipeline_id: str, organism_group: str):
        pass

    def sra_to_fasta_conversion(sra_id: str, pipeline_id: str, organism_group: str):
        pass

    def trimming_transcriptome(
        pipeline_id: str,
        sra_id: str,
        organism_group: str,
        trimming_type: TrimmingTypeEnum,
        input_path: str,
        output_path: str,
    ):
        pass
