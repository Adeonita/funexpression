from dataclasses import dataclass


@dataclass
class ConversionSraToFastaUseCaseInput:
    sra_id: str
    pipeline_id: str
    organism_group: str
