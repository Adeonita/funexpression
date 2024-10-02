import os
# import json
import logging
import subprocess


def create_folder_if_not_exist(run_id: str, directory_name: str, acession_number:str):
    temp_transcriptome = os.path.join(
        os.getcwd(), run_id, directory_name, acession_number
    )

    if not os.path.exists(temp_transcriptome):
        os.makedirs(temp_transcriptome)
    
    return temp_transcriptome
    

def remove_trash(dir: str):
    try:
        dir = os.path.join(os.getcwd() , "temp_files", dir)

        cmd = f"rm -rf {dir}"

        subprocess.call(cmd, shell=True)
        logging.info(f"remove sra file from {dir} ")

        return True
    except subprocess.SubprocessError as e:
        raise Exception(f"Occurred an error when try remove {dir}: {e}")




# def is_valid_sra_path(sra_file_path:str, sra_id:str):
#     logging.info(f"Validing path to: {sra_id}")

#     try:
#         subprocess.run(
#             ["vdb-validate", sra_file_path],
#             capture_output=True,
#             text=True,
#             check=True
#         )
        
#         return True

#     except subprocess.CalledProcessError as e:
#         raise(f"Error to validate file: {e.stderr}")


# def fasterq_dump(id: str, outdir: str):
#     try:

#         sra_path = f"./temp_files/{id}"

#         is_valid_sra = is_valid_sra_path(sra_path, id)

#         if is_valid_sra == True:
#             logging.info(f"Generating fastq for: {id}")

#             temp_outdir = f"./temp_files/{id}"
#             cmd = f"fasterq-dump {temp_outdir} --outdir {outdir}"

#             # cmd = f"fasterq-dump {temp_outdir} --outdir {outdir} -p"

#             # cmd = f"fasterq-dump {temp_outdir} --outdir {outdir} -p --concatenate-reads --include-technical"

#             subprocess.check_output(
#                 cmd,
#                 capture_output=True,
#                 text=True,
#                 check=True
#             )

#             logging.info(f"conversion from sra to fastq to {id} was finish the file can be finded in {outdir} ")
            
#             return True

#     except subprocess.CalledProcessError as e:
#         if e.output.startswith('error: {'):
#             error = json.loads(e.output[7:])
#             print(error['code'])
#             print(error['message'])
#         raise Exception(f"Error when extract {id}: {e.stderr}")


