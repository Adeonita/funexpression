from domain.entities.pipeline import Pipeline
from domain.entities.triplicate import OrganinsGroupEnum, SRAFile, Triplicate
from infrastructure.celery import aligner_transcriptome_task
from ports.infrastructure.storage.storage_path_port import StoragePathsPort


class TranscripomeAlignTask:
    def __init__(self, storage_paths: StoragePathsPort):
        self.storage_paths = storage_paths

    def align_transcriptomes(self, pipeline: Pipeline):
        self._align_triplicate(
            pipeline.control_organism,
            pipeline.id,
            pipeline.reference_genome.acession_number,
            OrganinsGroupEnum.CONTROL,
        )

        self._align_triplicate(
            pipeline.experiment_organism,
            pipeline.id,
            pipeline.reference_genome.acession_number,
            OrganinsGroupEnum.EXPERIMENT,
        )

    def _align_sra(
        self,
        sra_file: SRAFile,
        pipeline_id: str,
        genome_id: str,
        organism_group: OrganinsGroupEnum,
    ):
        sra_id = sra_file.acession_number

        genome_paths = self.storage_paths.get_genome_paths(genome_id)
        aligner_paths = self.storage_paths.get_aligner_path(
            pipeline_id, organism_group, sra_id
        )

        aligner_transcriptome_task(
            pipeline_id=pipeline_id,
            sra_id=sra_id,
            organism_group=organism_group,
            genome_index_path=genome_paths.index_path,
            trimed_transcriptome_path=aligner_paths.input,
            aligned_transcriptome_path=aligner_paths.output,
        )

    def _align_triplicate(
        self,
        triplicate: Triplicate,
        pipeline_id: str,
        genome_id: str,
        organism_group: OrganinsGroupEnum,
    ):
        self._align_sra(triplicate.srr_1, pipeline_id, genome_id, organism_group)
        self._align_sra(triplicate.srr_2, pipeline_id, genome_id, organism_group)
        self._align_sra(triplicate.srr_3, pipeline_id, genome_id, organism_group)
