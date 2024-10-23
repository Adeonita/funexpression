from infrastructure.celery import convert_sra_to_fasta_task


def send_sra_to_conversion_queue_in_bulk(sra_files, pipeline_id: str):
    for file in sra_files:
        sra_id = file[0]
        organism_group = file[1]

        convert_sra_to_fasta_task(sra_id, pipeline_id, organism_group)
