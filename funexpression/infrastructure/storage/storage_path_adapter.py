import os
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import OrganinsGroupEnum
from ports.infrastructure.storage.storage_path_port import (
    GenomePaths,
    Paths,
    StoragePathsPort,
)


class StoragePathsAdapter(StoragePathsPort):

    def get_genome_paths(self, genome_id: str) -> GenomePaths:
        return GenomePaths(
            fasta_path=f"./temp_files/{genome_id}.fna",
            gtf_path=f"./temp_files/{genome_id}.gtf",
            index_path=f"./temp_files/{genome_id}_index",
        )

    def get_converting_paths(self, pipeline_id, organism_group, sra_id):
        return Paths(
            input=f"pipelines/{pipeline_id}/DOWNLOADED/{organism_group}/{sra_id}.sra",
            # output=f"pipelines/{pipeline_id}/CONVERTED/{organism_group}/{sra_id}.fastq",
            output=f"pipelines/{pipeline_id}/CONVERTED/{organism_group}/{sra_id}",
        )

    def get_trimming_paths(self, pipeline_id, organism_group, sra_id) -> Paths:
        return Paths(
            input=f"./pipelines/{pipeline_id}/CONVERTED/{organism_group}/{sra_id}/{sra_id}.fastq",
            output=f"./pipelines/{pipeline_id}/TRIMMED/{organism_group}/{sra_id}.fq.gz",
        )

    def get_aligner_path(self, pipeline_id: str, organism_group: str, sra_id: str):
        return Paths(
            input=f"./pipelines/{pipeline_id}/TRIMMED/{organism_group}/{sra_id}.fq.gz",
            output=f"./pipelines/{pipeline_id}/ALIGNED/{organism_group}/{sra_id}_",
            # output=f"pipelines/{pipeline_id}/ALIGNER/{organism_group}/{sra_id}_Aligned.sortedByCoord.out.bam",
        )

    def get_counting_path(self, pipeline_id: str, organism_group: str, sra_id: str):
        return Paths(
            input=f"./pipelines/{pipeline_id}/ALIGNED/{organism_group}/{sra_id}_Aligned.sortedByCoord.out.bam",
            output=f"./pipelines/{pipeline_id}/COUNTED/{organism_group}/{sra_id}.txt",
        )

    def get_to_diffing_path(self, sra_files: dict, pipeline_id: str):

        event = {}
        index_counters = {}

        for identifier, group in sra_files:
            if group not in event:
                event[group] = {}
                index_counters[group] = 0

            index_counters[group] += 1
            key = f"srr_{index_counters[group]}"

            value = self.get_counting_path(
                pipeline_id=pipeline_id,
                organism_group=group.upper(),
                sra_id=identifier,
            ).output

            event[group][key] = value

        return event

    def get_diffed_file_paths(self, pipeline_id: str):
        return {
            "tsv_file": f"./pipelines/{pipeline_id}/DIFFED/diferential_expression_{pipeline_id}.tsv",
            "csv_file": f"./pipelines/{pipeline_id}/DIFFED/diferential_expression_{pipeline_id}.csv",
            "csv_to_graph": f"./pipelines/{pipeline_id}/DIFFED/diferential_expression_{pipeline_id}.csv",
            "vulcano_graph": f"./pipelines/{pipeline_id}/DIFFED/diferential_expression_{pipeline_id}.png",
            "heatmap_graph": f"./pipelines/{pipeline_id}/DIFFED/diferential_expression_{pipeline_id}.png",
        }

    def _create_outdir_if_not_exist(
        self, pipeline_id: str, step: str, group: str, acession_number=None
    ):
        if acession_number is not None:
            temp_files = os.path.join(
                "pipelines/", pipeline_id, step, group, acession_number
            )
        else:
            temp_files = os.path.join("pipelines/", pipeline_id, step, group)

        if not os.path.exists(temp_files):
            os.makedirs(temp_files)
            print(f"O diretório {temp_files} foi criado")

            return temp_files

        print(f"O diretório {temp_files} já existe")
        return None

    # def _create_outdir_if_not_exist(self, pipeline_id: str, step: str, group: str):
    #     temp_files = os.path.join("pipelines/", pipeline_id, step, group)

    #     if not os.path.exists(temp_files):
    #         os.makedirs(temp_files)
    #         return temp_files

    #     return None

    def _create_dirs(self):
        stages = [
            PipelineStageEnum.CONVERTED.value,
            PipelineStageEnum.TRIMMED.value,
            PipelineStageEnum.ALIGNED.value,
            PipelineStageEnum.COUNTED.value,
            PipelineStageEnum.DIFFED.value,
        ]

        groups = [OrganinsGroupEnum.EXPERIMENT.value, OrganinsGroupEnum.CONTROL.value]

        stage_combinations = []
        for stage in stages:
            if stage != PipelineStageEnum.DIFFED.value:
                for group in groups:
                    stage_combinations.append((stage, group))

        return stage_combinations

    def create_pipeline_directory_structure(self, pipeline_id: str):
        directories = self._create_dirs()
        for directory_stage, directory_organism_group in directories:
            diretory = os.path.join(
                "./pipelines/",
                pipeline_id,
                directory_stage,
                directory_organism_group,
            )

            if not os.path.exists(diretory):
                os.makedirs(diretory)

        return None
