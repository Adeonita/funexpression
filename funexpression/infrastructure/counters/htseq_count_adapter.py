import logging
import subprocess

from ports.infrastructure.counter.counter_port import CounterPort


class HTSeqCountAdapter(CounterPort):

    def count(
        self,
        aligned_file_path: str,
        gtf_genome_file_path: str,
        counted_file_path: str,
        sra_id: str,
    ):
        logging.info(f"Count genome for for: {sra_id}")

        try:
            cmd = f"""
                htseq-count -f bam \
                -r pos \
                -s no \
                -i gene_id \
                {aligned_file_path}  \
                {gtf_genome_file_path} > {counted_file_path}
            """

            subprocess.run(cmd, shell=True, check=True)

            logging.info(f"{sra_id} was counted with success")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Error when count {sra_id}: {e}")
