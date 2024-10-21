from ports.infrastructure.bio_database.genbank_port import GenBankPort


class GenBankAdapter(GenBankPort):
    def get_fasta_genome_from_ncbi(self, genome_id: str) -> str:

        return "fasta_genome_path"

    def get_gft_genome_from_ncbi(self, genome_id: str) -> str:

        return "gft_genome_path"
