from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from application.interfaces.expression_request_payload import ExpressionCalculateRequest
from infrastructure.clients.genbank_service import GenBankService
from infrastructure.clients.geo_service import GEOService

load_dotenv('../.env')

app = FastAPI()
router = APIRouter()

@router.post("/expression/calculate/")
def expression_calculate(request: ExpressionCalculateRequest):
    gene_id = request.reference_genome_acession_number
    transcriptome = request.control_organism.srr_acession_number_1
    GEOService().get_fasta_sequence(transcriptome)
    GenBankService().download_fasta_sequence_by_id(gene_id)
    return request

app.include_router(router)