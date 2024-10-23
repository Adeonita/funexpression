import logging
import os
import subprocess
from ports.infrastructure.bio_database.genbank_port import GenBankPort


class GenBankAdapter(GenBankPort):

    def _download_genome_files(self, genome_id: str, folder_name: str):
        cmd = f"datasets download genome accession {genome_id} --include gtf,protein --filename {folder_name}.zip"

        subprocess.run(cmd, shell=True)

        logging.info(f"The downloading to genome {genome_id} was executed with sucess")

    def _unzip_genome_files(
        self, folder_name: str, temp_directory: str, genome_id: str
    ):
        cmd_unzip = f"unzip {folder_name}.zip -d {temp_directory}"

        subprocess.run(cmd_unzip, shell=True)

        logging.info(f"The genome {genome_id} was unziped with sucess")

    def _remove_trash(
        self, trash_path: str, message: str, is_recursive=False, extension=None
    ):
        extension = extension if extension else ""

        if is_recursive:
            cmd_remove_trash = f"rm -rf {trash_path}{extension}"
            print(f"if cmd {cmd_remove_trash}")
        else:
            cmd_remove_trash = f"rm {trash_path}{extension}"
            print(f"else cmd {cmd_remove_trash}")

        subprocess.run(cmd_remove_trash, shell=True)

        logging.info(message)

    def _rename_genome_files(self, temp_directory: str, genome_id: str):
        rename_gtf = f"mv ./{temp_directory}/ncbi_dataset/data/{genome_id}/genomic.gtf ./temp_files/"
        rename_fasta = f"mv ./{temp_directory}/ncbi_dataset/data/{genome_id}/protein.faa ./temp_files/"

        subprocess.run(rename_gtf, shell=True)
        subprocess.run(rename_fasta, shell=True)

    def _move_files(self, genome_id: str):
        cmd_move_gtf = f"mv ./temp_files/genomic.gtf ./temp_files/{genome_id}.gtf"
        cmd_move_fasta = f"mv ./temp_files/protein.faa ./temp_files/{genome_id}.faa"

        subprocess.run(cmd_move_gtf, shell=True)
        subprocess.run(cmd_move_fasta, shell=True)

    def _get_final_pahts_genome_files(self, genome_id: str):
        return {
            "gtf_path": f"./temp_files/{genome_id}.gtf",
            "fasta_path": f"./temp_files/{genome_id}.faa",
        }

    def get_gtf_and_fasta_genome_from_ncbi(self, genome_id: str):
        try:
            logging.info(f"Currently downloading {genome_id} with prefetch")

            is_already_downloaded = self.is_already_downloaded(genome_id)

            if is_already_downloaded:
                logging.info("Genome already downloaded, noting do is necessary")
                return is_already_downloaded

            folder_name = f"genome_{genome_id}"
            temp_directory = self._create_outdir_if_not_exist(folder_name)

            if temp_directory:
                self._download_genome_files(genome_id, folder_name)

                self._unzip_genome_files(folder_name, temp_directory, genome_id)

                self._remove_trash(
                    trash_path=folder_name,
                    message=f"The genome {genome_id} zip folder was removed with sucess",
                    is_recursive=False,
                    extension=".zip",
                )

                self._rename_genome_files(temp_directory, genome_id)

                self._move_files(genome_id)

                self._remove_trash(
                    trash_path=temp_directory,
                    message=f"The genome {genome_id} folder was removed with sucess",
                    is_recursive=True,
                )

                return self._get_final_pahts_genome_files(genome_id)
        except subprocess.SubprocessError as e:
            print(e)
            raise Exception(f"Occurred an error when try download: {genome_id}")

    def _create_outdir_if_not_exist(self, directory_name: str):
        temp_files = os.path.join("temp_files/", directory_name)

        if not os.path.exists(temp_files):
            os.makedirs(temp_files)
            return temp_files

        return None

    def is_already_downloaded(self, genome_id: str):
        paths = self._get_final_pahts_genome_files(genome_id)
        gtf_path = paths["gtf_path"]
        fasta_path = paths["fasta_path"]

        if os.path.exists(gtf_path) and os.path.exists(fasta_path):
            return {
                "gtf_path": gtf_path,
                "fasta_path": fasta_path,
            }

        return False
