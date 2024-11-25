from dataclasses import dataclass


@dataclass
class PipelineTriplicate:
    srr_acession_number_1: str
    srr_acession_number_2: str
    srr_acession_number_3: str


@dataclass
class PipelineCreateUseCaseInput:
    name: str
    email: str
    run_id: str
    p_adj: float
    log_2_fold_change_threshold: float
    control_organism: PipelineTriplicate
    experiment_organism: PipelineTriplicate
    reference_genome_acession_number: str
