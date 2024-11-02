from domain.entities.pipeline import Pipeline
from domain.entities.triplicate import OrganinsGroupEnum, SRAFile, Triplicate
from infrastructure.celery import download_sra_task


class TranscriptomeDownloadTask:
    def download_transcriptomes(self, pipeline: Pipeline):
        self._download_triplicate(
            pipeline.control_organism, pipeline.id, OrganinsGroupEnum.CONTROL
        )

        self._download_triplicate(
            pipeline.experiment_organism, pipeline.id, OrganinsGroupEnum.EXPERIMENT
        )

    def _download_triplicate(
        self, tri: Triplicate, pipeline_id: str, organism_group: OrganinsGroupEnum
    ):
        self._download_sra(tri.srr_1, pipeline_id, organism_group)
        self._download_sra(tri.srr_2, pipeline_id, organism_group)
        self._download_sra(tri.srr_3, pipeline_id, organism_group)

    def _download_sra(
        self, sra_file: SRAFile, pipeline_id: str, organism_group: OrganinsGroupEnum
    ):
        sra_id = sra_file.acession_number

        download_sra_task(sra_id, pipeline_id, organism_group)
