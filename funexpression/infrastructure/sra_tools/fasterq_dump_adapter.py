import os
import logging
import subprocess


class FasterqDumpAdapter:
    def _is_valid_sra_path(self, sra_file_path: str, sra_id: str):
        print(f"Validing path to: {sra_id} --> {sra_file_path}")

        try:
            cmd = f"vdb-validate {sra_file_path}"

            subprocess.run(cmd, shell=True)

            return True

        except subprocess.CalledProcessError as e:
            raise (f"Error to validate file: {e.stderr}")

    def dump_sra_to_fasta(self, id: str, outdir: str):
        try:

            sra_path = os.path.join("temp_files/")

            is_valid_sra = self._is_valid_sra_path(sra_path, id)

            if is_valid_sra == True:
                logging.info(f"Generating fastq for: {id}")

                input_file_dir = f"temp_files/{id}"

                cmd = f"fasterq-dump {input_file_dir} --outdir {outdir}"

                subprocess.run(cmd, shell=True, check=True)

                logging.info(
                    f"conversion from sra to fastq to {id} was finish the file can be finded in {outdir} "
                )

                return True
            else:
                print(f"sra_path {sra_path} is invalid")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Error when extract {id}: {e}")
