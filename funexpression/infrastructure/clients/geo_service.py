import json
import logging
import subprocess

from infrastructure.clients.commands import create_folder_if_not_exist

class GEOService:
    def _is_valid_sra_path(sra_file_path:str, sra_id:str):
        logging.info(f"Validing path to: {sra_id}")

        try:
            subprocess.run(
                ["vdb-validate", sra_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            return True

        except subprocess.CalledProcessError as e:
            raise(f"Error to validate file: {e.stderr}")

    def _prefetch(self, id):
        try:
            logging.info(f"Currently downloading {id} with prefetch")

            cmd = f"prefetch {id} --output-directory temp_files"

            subprocess.check_output(cmd, capture_output=True, text=True, check=True)

            logging.info(f"The downloading to {id} was executed with sucess")

            return True

        except subprocess.SubprocessError as e:
            if e.output.startswith('error: {'):
                error = json.loads(e.output[7:])
                print(error['code'])
                print(error['message'])
            raise Exception(f"Occurred an error when try download: {id}")

    def _fasterq_dump(self, id: str, outdir: str):
        try:

            sra_path = f"./temp_files/{id}"

            is_valid_sra = self._is_valid_sra_path(sra_path, id)

            if is_valid_sra == True:
                logging.info(f"Generating fastq for: {id}")

                temp_outdir = f"./temp_files/{id}"
                cmd = f"fasterq-dump {temp_outdir} --outdir {outdir}"

                subprocess.check_output(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )

                logging.info(f"conversion from sra to fastq to {id} was finish the file can be finded in {outdir} ")
                
                return True

        except subprocess.CalledProcessError as e:
            if e.output.startswith('error: {'):
                error = json.loads(e.output[7:])
                print(error['code'])
                print(error['message'])
            raise Exception(f"Error when extract {id}: {e.stderr}")

    def get_fasta_sequence_from_ncbi(self, run_id, sra_id, group):
        logging.info("Starting download fastq sequence from ncbi ")

        try:
            self._prefetch(sra_id)
            outdir = create_folder_if_not_exist(run_id, group, sra_id)
            self._fasterq_dump(sra_id, outdir)
            # remove_trash(sra_id)

        except Exception as e:
            return f"there was an error when downloading fasta sequence {e}"
