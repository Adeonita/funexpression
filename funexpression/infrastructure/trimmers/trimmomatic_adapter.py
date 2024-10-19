import logging
import subprocess
from ports.infrastructure.trimmer.trimmer_port import TrimmerPort


class TrimmomaticAdapter(TrimmerPort):

    def trim(
        self, sra_id: str, trimming_type: str, input_path: str, output_path: str
    ) -> None:
        try:
            logging.info(f"Trimming fastq for: {sra_id}")

            cmd = f"java -jar /trimmomatic/trimmomatic-0.39.jar {trimming_type} -phred33 {input_path} {output_path} ILLUMINACLIP:/trimmomatic/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"

            subprocess.run(cmd, shell=True, check=True)

            logging.info(f"{sra_id} was trimmed with sucess")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Error when trim {sra_id}: {e}")
