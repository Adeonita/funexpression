from pydantic import BaseModel


class Triplicate(BaseModel):
    srr_acession_number_1: str
    srr_acession_number_2: str
    srr_acession_number_3: str


class ExpressionCalculateRequest(BaseModel):
    name: str
    email: str
    p_adj: float
    log_2_fold_change_threshold: float
    control_organism: Triplicate
    experiment_organism: Triplicate
    reference_genome_acession_number: str
