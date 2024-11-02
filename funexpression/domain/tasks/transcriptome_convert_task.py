from domain.entities.pipeline import Pipeline
from domain.entities.triplicate import OrganinsGroupEnum, SRAFile, Triplicate
from infrastructure.celery import convert_sra_to_fasta_task


class TranscripomeConvertTask:
    def _convert_sra_to_fasta(
        self, sra_file: SRAFile, pipeline_id: str, organism_group: str
    ):
        sra_id = sra_file.acession_number

        convert_sra_to_fasta_task(sra_id, pipeline_id, organism_group)

    def _convert_triplicate(
        self, tri: Triplicate, pipeline_id: str, organism_group: str
    ):
        self._convert_sra_to_fasta(tri.srr_1, pipeline_id, organism_group)
        self._convert_sra_to_fasta(tri.srr_2, pipeline_id, organism_group)
        self._convert_sra_to_fasta(tri.srr_3, pipeline_id, organism_group)

    def _convert_transcriptomes(self, pipeline: Pipeline):
        self._convert_triplicate(
            pipeline.experiment_organism, pipeline.id, OrganinsGroupEnum.EXPERIMENT
        )
        self._convert_triplicate(
            pipeline.control_organism, pipeline.id, OrganinsGroupEnum.CONTROL
        )