from enum import Enum
import json
import os
from infrastructure.sra_tools.fasterq_dump_adapter import FasterqDumpAdapter
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)


class GroupsEnum(Enum):
    CONTROL = "CONTROL"
    EXPERIMENT = "EXPERIMENT"


class ConversionSraToFastaUseCase:
    def __init__(
        self,
        fasterq_dump_adapter: FasterqDumpAdapter,
        pipeline_repository: PipelineRepositoryPort,
    ):
        self.pipeline_repository = pipeline_repository
        self.fasterq_dump_adapter = fasterq_dump_adapter

    # todo já receber por parametro o controle e o experimento ou mantenho assim para buscar?
    def execute(self, pipeline_id: str):
        pipeline = self.pipeline_repository.get_sra_files(pipeline_id)

        MAX_SIZE = 2

        cotrol_organism_list = pipeline["control"]
        experiment_organism_list = pipeline["experiment"]
        all_organisms = cotrol_organism_list + experiment_organism_list

        sra_files = self._split_list(all_organisms, MAX_SIZE)

        for elements in sra_files:
            for element in elements:
                group = self._get_group(
                    element, cotrol_organism_list, experiment_organism_list
                )
                output_dir = self._create_folder_if_not_exist(
                    pipeline_id, group, element
                )

                self.fasterq_dump_adapter.dump_sra_to_fasta(element, output_dir)

    def _split_list(self, list_, max_size):
        return [list_[i : i + max_size] for i in range(0, len(list_), max_size)]

    def _get_group(self, srr, control_list, experiment_list):
        if srr in control_list:
            return GroupsEnum.CONTROL.value
        elif srr in experiment_list:
            return GroupsEnum.EXPERIMENT.value

    def _create_folder_if_not_exist(
        self, pipeline_id: str, group: str, acession_number: str
    ):
        temp_files = os.path.join("pipelines/", pipeline_id, group, acession_number)

        if not os.path.exists(temp_files):
            os.makedirs(temp_files)

        return temp_files
