import os
import subprocess

class GEOService():
    def _create_folder_if_not_exist(self, directory_name: str, acession_number:str):
            temp_transcriptome = os.path.join(
                os.getcwd(), directory_name, f'results_{acession_number}'
            )

            if not os.path.exists(temp_transcriptome):
                os.makedirs(temp_transcriptome)
            
            return temp_transcriptome

    def get_fasta_sequence(self, sra_number):

        sra_numbers = [sra_number]

        for sra_id in sra_numbers:
            print ("Generating fastq for: " + sra_id)
            fastq_dump=  f"fastq-dump --split-files --outdir {self._create_folder_if_not_exist('transcriptome', sra_id)} {sra_id}"
            print ("The command used was: " + fastq_dump)
            subprocess.call(fastq_dump, shell=True)
