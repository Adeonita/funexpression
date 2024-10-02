import json
import logging
import subprocess
from ports.infrastructure.bio_database.geo_adapter_port import GeoAdapterPort


class GeoAdapter(GeoAdapterPort):

    def _prefetch(self, sra_id) -> str:
        try:
            sra_path = f"temp_files/{sra_id}"
            logging.info(f"Currently downloading {sra_id} with prefetch")

            cmd = f"prefetch {sra_id} --output-directory temp_files"

            subprocess.run(cmd, shell=True)

            logging.info(f"The downloading to {sra_id} was executed with sucess")

            return sra_path

        except subprocess.SubprocessError as e:
            print(e)
            if e.output.startswith("error: {"):
                error = json.loads(e.output[7:])
                print(error["code"])
                print(error["message"])
            raise Exception(f"Occurred an error when try download: {id}")

    def get_sra_sequence_from_ncbi(self, sra_id: str):
        logging.info("Starting download sra sequence from ncbi ")
        self._prefetch(sra_id)
