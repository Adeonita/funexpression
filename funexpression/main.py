from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI


from application.helpers.helper import get_user_name_by_email
from application.interfaces.expression_request_payload import ExpressionCalculateRequest

from domain.factories.pipeline.pipeline_create_usecase_factory import (
    PipelineCreateUseCaseFactory,
)
from domain.usecases.pipeline.input.pipeline_create_input import (
    PipelineCreateUseCaseInput,
    PipelineTriplicate,
)

import uuid

load_dotenv("../.env")

app = FastAPI()
router = APIRouter()


@router.post("/expression/calculate/")
def expression_calculate(request: ExpressionCalculateRequest):
    user_name = get_user_name_by_email(request.email)
    run_id = f"{user_name}-{str(uuid.uuid4())}"

    pipeline_create_usecase = PipelineCreateUseCaseFactory.create()

    pipeline_c_input = PipelineCreateUseCaseInput(
        name=request.name,
        email=request.email,
        run_id=run_id,
        p_adj=request.p_adj,
        log_2_fold_change_threshold=request.log_2_fold_change_threshold,
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

    created_pipeline = pipeline_create_usecase.execute(pipeline_c_input)

    return created_pipeline


app.include_router(router)
