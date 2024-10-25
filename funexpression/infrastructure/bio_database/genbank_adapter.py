import json
import logging
import os
import subprocess
from ports.infrastructure.bio_database.genbank_port import GenBankPort


class GenBankAdapter(GenBankPort):

    def _download_genome_files(self, genome_id: str, folder_name: str):
        cmd = f"datasets download genome accession {genome_id} --include gtf,genome --filename {folder_name}.zip"

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
        else:
            cmd_remove_trash = f"rm {trash_path}{extension}"

        subprocess.run(cmd_remove_trash, shell=True)

        logging.info(message)

    def _rename_file(self, old_path: str, new_path: str):
        cmd_rename = f"mv {old_path} {new_path}"

        subprocess.run(cmd_rename, shell=True)

    def _move_files(self, genome_files_path):
        self._move_file(old_path=genome_files_path["gtf_path"], new_path="./temp_files")

        self._move_file(
            old_path=genome_files_path["fasta_path"], new_path="./temp_files"
        )

    def _move_file(self, old_path: str, new_path: str):
        cmd_move = f"mv {old_path} {new_path}"

        subprocess.run(cmd_move, shell=True)

    def _get_final_pahts_genome_files(self, genome_id: str):
        return {
            "gtf_path": f"./temp_files/{genome_id}.gtf",
            "fasta_path": f"./temp_files/{genome_id}.fasta",
        }

    def _get_genomes_paths_by_dataset_catalog(self, genome_id: str):
        ncbi_dataset_path = f"./temp_files/genome_{genome_id}/ncbi_dataset/data"
        dataset_catalog_file_path = f"{ncbi_dataset_path}/dataset_catalog.json"
        with open(dataset_catalog_file_path, "r") as file:
            data = json.load(file)

            genome_files = data["assemblies"][1]["files"]

            split_in = f"{genome_id}/"
            fasta_genome_file_name = (genome_files[0]["filePath"]).split(split_in, 1)[
                -1
            ]

            gtf_genome_file_name = (genome_files[1]["filePath"]).split(split_in, 1)[-1]

            # fmt: off
            actual_fasta_path = f"{ncbi_dataset_path}/{genome_id}/{fasta_genome_file_name}"
            actual_gtf_path = f"{ncbi_dataset_path}/{genome_id}/{gtf_genome_file_name}"

            new_fasta_path = f"{ncbi_dataset_path}/{genome_id}/{genome_id}.fna"
            new_gtf_path = f"{ncbi_dataset_path}/{genome_id}/{genome_id}.gtf"

            self._rename_file(old_path=actual_fasta_path, new_path=new_fasta_path)
            self._rename_file(old_path=actual_gtf_path, new_path=new_gtf_path)

            return {
                "gtf_path": new_gtf_path,
                "fasta_path": new_fasta_path,
            }

    def get_gtf_and_fasta_genome_from_ncbi(self, genome_id: str):
        try:
            logging.info(f"Currently downloading {genome_id} with ncbi dataset")

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

                genome_files_path = self._get_genomes_paths_by_dataset_catalog(
                    genome_id
                )

                self._move_files(genome_files_path)

                self._remove_trash(
                    trash_path=f"./temp_files/genome_{genome_id}",
                    message=f"The genome {genome_id} folder was removed with sucess",
                    is_recursive=True,
                )

                return self._get_final_pahts_genome_files(genome_id)

            genome_files_path = self._get_genomes_paths_by_dataset_catalog(genome_id)

            self._move_files(genome_files_path)

            self._remove_trash(
                trash_path=f"./temp_files/genome_{genome_id}",
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
