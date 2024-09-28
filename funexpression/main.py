from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from aplication.helpers.helper import get_srr_list, get_user_name_by_email
from aplication.interfaces.expression_request_payload import ExpressionCalculateRequest
# from infrastructure.clients.genbank_service import GenBankService
# from infrastructure.clients.geo_service import GEOService
from infrastructure.clients.geo_service import get_fasta_sequence
import uuid

load_dotenv('../.env')

app = FastAPI()
router = APIRouter()

@router.post("/expression/calculate/")
def expression_calculate(request: ExpressionCalculateRequest):
    user = get_user_name_by_email(request.email)
    gene_id = request.reference_genome_acession_number
    control_transcriptomes = get_srr_list(request.control_organism)
    experiment_transcriptomes = get_srr_list(request.experiment_organism)
    run_id = f"{user}-{str(uuid.uuid4())}"

    for c_transcriptome, e_transcriptome in zip(control_transcriptomes, experiment_transcriptomes):
        get_fasta_sequence.delay(run_id, 'transcriptome_control', c_transcriptome)
        # get_fasta_sequence(run_id, 'transcriptome_experiment', e_transcriptome)

    # GenBankService().download_fasta_sequence_by_id(gene_id)
    return control_transcriptomes

app.include_router(router)