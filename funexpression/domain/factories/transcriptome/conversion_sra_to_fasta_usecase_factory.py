from domain.usecases.conversion.conversion_sra_to_fasta_usecase import (
    ConversionSraToFastaUseCase,
)
from infrastructure.repositories.pipeline_repository_mongo import (
    PipelineRepositoryMongo,
)
from infrastructure.sra_tools.fasterq_dump_adapter import FasterqDumpAdapter


class ConversionSraToFastaUseCaseFactory:

    @staticmethod
    def create():
        fasterq_dump_adapter = FasterqDumpAdapter()
        pipeline_repository = PipelineRepositoryMongo()

        return ConversionSraToFastaUseCase(fasterq_dump_adapter, pipeline_repository)
