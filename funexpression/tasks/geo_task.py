from infrastructure.celery import app
from infrastructure.clients.geo_service import GEOService


@app.task
def get_fasta_sequence(run_id, group, sra_id):

    try:
        geo = GEOService()
        geo.get_fasta_sequence_from_ncbi(run_id, group, sra_id)


    except Exception as e:
        return f"there was an error when downloading fasta sequence {e}"
