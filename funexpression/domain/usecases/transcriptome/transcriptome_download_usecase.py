from domain.entities.triplicate import SRAFileStatusEnum
from domain.usecases.transcriptome.input.transcriptome_download_usecase_input import (
    TranscriptomeDownloadUseCaseInput,
)
from ports.infrastructure.bio_database.geo_adapter_port import GeoAdapterPort
from ports.infrastructure.repositories.pipeline_repository_port import (
    PipelineRepositoryPort,
)


class TranscriptomeDownloadUseCase:

    def __init__(
        self, geo_adapter: GeoAdapterPort, pipeline_repository: PipelineRepositoryPort
    ):
        self.geo_adapter = geo_adapter
        self.pipeline_repository = pipeline_repository

    def execute(self, input: TranscriptomeDownloadUseCaseInput) -> str:
        sra_path = self.geo_adapter.get_sra_sequence_from_ncbi(input.sra_id)
        self.pipeline_repository.update_sra_file_status(
            pipeline_id=input.pipeline_id,
            sra_id=input.sra_id,
            status=SRAFileStatusEnum.OK,
        )

        return sra_path

    def _is_all_file_download_completed(self):
        pass
