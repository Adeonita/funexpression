from infrastructure.celery import app
from infrastructure.clients.geo_service import GEOService
from domain.factories.transcriptome.transcriptome_download_usecase_factory import TranscriptomeDownloadUseCaseFactory

@app.task(queue='geo_sra_download')
def sra_transcriptome_download(sra_id: str):
    try:
        transcriptome_download_usecase = TranscriptomeDownloadUseCaseFactory.create()
        transcriptome_download_usecase.execute(sra_id)
    except Exception as e:
        return f"there was an error when downloading sra sequence {e}"

@app.task(queue="geo_control")
def get_fasta_sequence_control(run_id, sra_id, group):

    try:
        geo = GEOService()
        geo.get_fasta_sequence_from_ncbi(run_id, sra_id, group)


    except Exception as e:
        return f"there was an error when downloading fasta sequence {e}"
    
@app.task(queue='geo_experiment')
def get_fasta_sequence_experiment(run_id, sra_id, group):

    try:
        geo = GEOService()
        geo.get_fasta_sequence_from_ncbi(run_id, sra_id, group)


    except Exception as e:
        return f"there was an error when downloading fasta sequence {e}"
