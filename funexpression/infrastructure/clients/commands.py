import os
import logging
import subprocess


def create_folder_if_not_exist(run_id: str, directory_name: str, acession_number:str):
    temp_transcriptome = os.path.join(
        os.getcwd(), run_id, directory_name, acession_number
    )

    if not os.path.exists(temp_transcriptome):
        os.makedirs(temp_transcriptome)
    
    return temp_transcriptome

def run_command(command: str):
    subprocess.call(command, shell=True)

def prefetch(id):
    logging.info(f"Currently downloading {id} with prefetch")

    cmd = f"prefetch {id} --output-directory temp_files"

    run_command(cmd)

    logging.info(f"The downloading to {id} was executed with sucess")

    return

def is_valid_sra_path(sra_file_path):
    try:
        subprocess.run(
            ["vdb-validate", sra_file_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        return True

    except subprocess.CalledProcessError as e:
        logging.info(f"Error to validate file: {e.stderr}")
        return False

def fasterq_dump(id: str, outdir:str):
    sra_path = f"./temp_files/{id}"

    is_valid_sra = is_valid_sra_path(sra_path)

    if is_valid_sra == True:
        logging.info(f"Generating fastq for: {id}")

        temp_outdir = f"./temp_files/{id}"
        cmd = f"fasterq-dump {temp_outdir} --outdir {outdir}"

        run_command(cmd)

        logging.info(f"conversion from sra to fastq to {id} was finish the file can be finded in {outdir} ")
        
        return


def remove_trash(dir: str):
    dir = os.path.join(os.getcwd() , "temp_files", dir)

    cmd = f"rm -rf {dir}"

    run_command(cmd)

    logging.info(f"remove sra file from {dir} ")

    return

