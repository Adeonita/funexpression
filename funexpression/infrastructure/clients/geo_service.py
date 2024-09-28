import os
import subprocess

from infrastructure.celery import app

def _create_folder_if_not_exist(run_id, directory_name: str, acession_number:str):
    temp_transcriptome = os.path.join(
        os.getcwd(), run_id, directory_name, acession_number
    )

    if not os.path.exists(temp_transcriptome):
        os.makedirs(temp_transcriptome)
    
    return temp_transcriptome

@app.task
def get_fasta_sequence(run_id, group, sra_id):

    print(f"Generating fastq for: {sra_id}")
    outdir = _create_folder_if_not_exist(run_id, group, sra_id)
    fastq_dump = f"fastq-dump --outdir {outdir} {sra_id}"

    print(f"The command used was: {fastq_dump} ")
    subprocess.call(fastq_dump, shell=True)
