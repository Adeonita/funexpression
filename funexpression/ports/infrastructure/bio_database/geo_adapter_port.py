from typing import Protocol


class GeoAdapterPort(Protocol):
    
    def get_sra_sequence_from_ncbi(self, sra_id: str) -> str:
        pass