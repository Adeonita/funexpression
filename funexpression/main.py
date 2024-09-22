from fastapi import APIRouter, FastAPI
from application.interfaces.expression_request_payload import ExpressionCalculateRequest
from infraestructure.clients.genbank_service import download_fasta_sequence_by_id

app = FastAPI()
router = APIRouter()

@router.post("/expression/calculate/")
def expression_calculate(request: ExpressionCalculateRequest):
    gene_id = request.reference_genome_acession_number
    genome = download_fasta_sequence_by_id(gene_id)
    return request

app.include_router(router)