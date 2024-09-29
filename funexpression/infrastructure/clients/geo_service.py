import logging

from infrastructure.clients.commands import create_folder_if_not_exist, fasterq_dump, prefetch, remove_trash

class GEOService:

    def get_fasta_sequence_from_ncbi(self, run_id, group, sra_id):
        logging.info("Starting download fastq sequence from ncbi ")

        try:
            prefetch(sra_id)
            outdir = create_folder_if_not_exist(run_id, group, sra_id)
            fasterq_dump(sra_id, outdir)
            remove_trash(sra_id)

        except Exception as e:
            return f"there was an error when downloading fasta sequence {e}"
