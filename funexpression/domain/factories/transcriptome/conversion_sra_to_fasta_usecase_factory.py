from domain.usecases.transcriptome.conversion_sra_to_fasta_usecase import (
    ConversionSraToFastaUseCase,
)
from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)
from infrastructure.sra_tools.fasterq_dump_adapter import FasterqDumpAdapter
from infrastructure.storage.storage_path_adapter import StoragePathsAdapter


class ConversionSraToFastaUseCaseFactory:

    @staticmethod
    def create():
        fasterq_dump_adapter = FasterqDumpAdapter()
        storage_paths = StoragePathsAdapter()
        pipeline_repository = PipelineRepositoryMongo()

        return ConversionSraToFastaUseCase(
            fasterq_dump_adapter, storage_paths, pipeline_repository
        )
