from celery import Celery

app = Celery(
    "geo",
    broker="pyamqp://admin:pass@rabbitmq:5672//",
    include=[
        # 'tasks.geo_task'
        "infrastructure.messaging.task"
    ],
)


def convert_sra_to_fasta_task(sra_id, pipeline_id, organism_group):
    app.send_task(
        "infrastructure.messaging.task.sra_to_fasta_conversion",
        args=(sra_id, pipeline_id, organism_group),
        queue="sra_to_fasta_conversion",
    )


def download_sra_task(sra_id, pipeline_id, organism_group):
    app.send_task(
        "infrastructure.messaging.task.sra_transcriptome_download",
        args=(sra_id, pipeline_id, organism_group),
        queue="geo_sra_download",
    )


def download_genome_task(genome_id: str, pipeline_id: str):
    app.send_task(
        "infrastructure.messaging.task.genome_download",
        args=(genome_id, pipeline_id),
        queue="genbank_ncbi_download",
    )


def trimming_transcriptome_task(
    pipeline_id, sra_id, organism_group, trimming_type, input_path, output_path
):
    app.send_task(
        "infrastructure.messaging.task.trimming_transcriptome",
        args=(
            pipeline_id,
            sra_id,
            organism_group,
            trimming_type,
            input_path,
            output_path,
        ),
        queue="trimming_transcriptome",
    )
