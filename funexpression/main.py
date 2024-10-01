from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from aplication.helpers.helper import get_srr_list, get_user_name_by_email
from aplication.interfaces.expression_request_payload import ExpressionCalculateRequest

# from infrastructure.clients.genbank_service import GenBankService
from domain.factories.pipeline.pipeline_create_usecase_factory import (
    PipelineCreateUseCaseFactory,
)
from domain.factories.transcriptome.transcriptome_download_usecase_factory import (
    TranscriptomeDownloadUseCaseFactory,
)
from domain.usecases.pipeline.input.pipeline_create_input import (
    PipelineCreateUseCaseInput,
    PipelineTriplicate,
)
from tasks.geo_task import get_fasta_sequence_control, get_fasta_sequence_experiment

import uuid

load_dotenv("../.env")

app = FastAPI()
router = APIRouter()


@router.post("/expression/calculate/")
def expression_calculate(request: ExpressionCalculateRequest):
    user = get_user_name_by_email(request.email)
    gene_id = request.reference_genome_acession_number
    control_transcriptomes = get_srr_list(request.control_organism)
    experiment_transcriptomes = get_srr_list(request.experiment_organism)
    run_id = f"{user}-{str(uuid.uuid4())}"
    sra_ids = control_transcriptomes + experiment_transcriptomes

    pipeline_create_usecase = PipelineCreateUseCaseFactory.create()

    pipeline_c_input = PipelineCreateUseCaseInput(
        email=request.email,
        run_id=run_id,
        experiment_organism=PipelineTriplicate(
            srr_acession_number_1=request.experiment_organism.srr_acession_number_1,
            srr_acession_number_2=request.experiment_organism.srr_acession_number_2,
            srr_acession_number_3=request.experiment_organism.srr_acession_number_3,
        ),
        control_organism=PipelineTriplicate(
            srr_acession_number_1=request.control_organism.srr_acession_number_1,
            srr_acession_number_2=request.control_organism.srr_acession_number_2,
            srr_acession_number_3=request.control_organism.srr_acession_number_3,
        ),
        reference_genome_acession_number=request.reference_genome_acession_number,
    )

    pipeline_create_usecase.execute(pipeline_c_input)

    # for c_transcriptome, e_transcriptome in zip(control_transcriptomes, experiment_transcriptomes):

    #     # get_fasta_sequence_control.delay(run_id, c_transcriptome, 'transcriptome_control')
    #     # get_fasta_sequence_experiment.delay(run_id, e_transcriptome, 'transcriptome_experiment')

    # GenBankService().download_fasta_sequence_by_id(gene_id)
    return control_transcriptomes


app.include_router(router)
