import logging
import subprocess
from ports.infrastructure.aligner.aligner_port import AlignerPort


class RnaStarAdapter(AlignerPort):
    THREAD_NUMBER = 0

    def __init__(self):
        self.THREAD_NUMBER = 4

    def generate_genome_index(
        self,
        genome_id: str,
        gtf_genome_path: str,
        fasta_genome_path: str,
        index_genome_output_path: str,
    ) -> str:
        try:
            logging.info(f"Generating genome index for: {genome_id}")

            cmd = f"""
                    STAR --runThreadN {self.THREAD_NUMBER} \
                    --runMode genomeGenerate \
                    --genomeDir {index_genome_output_path} \
                    --genomeFastaFiles {fasta_genome_path} \
                    --sjdbGTFfile {gtf_genome_path} \
                    --sjdbOverhang 100
                """

            subprocess.run(cmd, shell=True, check=True)

            logging.info(
                f"Genome index for {genome_id} was generated with success and can be found at {index_genome_output_path}"
            )

            return index_genome_output_path

        except subprocess.CalledProcessError as e:
            raise Exception(
                f"Error when generate genome index for {fasta_genome_path}: {e}"
            )

    def align(
        self,
        sra_id: str,
        genome_index_path: str,
        input_path: str,
        output_path: str,
    ) -> None:
        try:
            logging.info(f"Aligner genome for for: {sra_id}")

            cmd = f"""
                    STAR --runThreadN {self.THREAD_NUMBER} \
                    --genomeDir {genome_index_path} \
                    --readFilesIn {input_path} \
                    --readFilesCommand zcat \
                    --outFileNamePrefix {output_path} \
                    --outSAMtype BAM SortedByCoordinate
                """

            subprocess.run(cmd, shell=True, check=True)

            logging.info(f"{sra_id} was aligned with success")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Error when align {sra_id}: {e}")
