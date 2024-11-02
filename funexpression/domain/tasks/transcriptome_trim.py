from domain.entities.pipeline import Pipeline
from domain.entities.triplicate import OrganinsGroupEnum, SRAFile, Triplicate
from infrastructure.celery import trimming_transcriptome_task


class TranscriptomeTrimTask:    
    def _trimming_sra(
        self, sra_file: SRAFile, pipeline_id: str, organism_group: OrganinsGroupEnum
    ):
        sra_id = sra_file.acession_number

        input_path = self.storage_paths.get_trimming_paths(
            pipeline_id, organism_group, sra_id
        ).input
        output_path = self.storage_paths.get_trimming_paths(
            pipeline_id, organism_group, sra_id
        ).output

        trimming_transcriptome_task(
            pipeline_id=pipeline_id,
            sra_id=sra_id,
            organism_group=organism_group,
            trimming_type="SE",
            input_path=input_path,
            output_path=output_path,
        )

    def _trimming_triplicate(
        self,
        triplicate: Triplicate,
        pipeline_id: str,
        organism_group: OrganinsGroupEnum,
    ):
        self._trimming_sra(triplicate.srr_1, pipeline_id, organism_group)
        self._trimming_sra(triplicate.srr_2, pipeline_id, organism_group)
        self._trimming_sra(triplicate.srr_3, pipeline_id, organism_group)

    def _trimming_transcriptomes(self, pipeline: Pipeline):
        self._trimming_triplicate(
            pipeline.control_organism, pipeline.id, OrganinsGroupEnum.CONTROL
        )

        self._trimming_triplicate(
            pipeline.experiment_organism, pipeline.id, OrganinsGroupEnum.EXPERIMENT
        )