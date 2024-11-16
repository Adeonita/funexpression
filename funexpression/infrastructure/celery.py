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


def generate_index_genome_task(
    pipeline_id, genome_id, gtf_genome_path, fasta_genome_path, index_genome_output_path
):
    print("Sending to the generate index genome queue...")

    app.send_task(
        "infrastructure.messaging.task.generate_index_genome",
        args=(
            pipeline_id,
            genome_id,
            gtf_genome_path,
            fasta_genome_path,
            index_genome_output_path,
        ),
        queue="generate_index_genome",
    )

    print("Message sent to the generate index genome queue!")


def aligner_transcriptome_task(
    pipeline_id,
    sra_id,
    # genome_id, TODO: add that
    organism_group,
    genome_index_path,
    trimed_transcriptome_path,
    aligned_transcriptome_path,
):
    print("Sending to the aligner genome queue...")

    app.send_task(
        "infrastructure.messaging.task.aligner_transcriptome",
        args=(
            pipeline_id,
            sra_id,
            # genome_id,
            organism_group,
            genome_index_path,
            trimed_transcriptome_path,
            aligned_transcriptome_path,
        ),
        queue="aligner_transcriptome",
    )

    print("Message sent to the aligner genome queue!")


def counter_transcriptome_task(
    pipeline_id,
    sra_id,
    organism_group,
    aligned_transcriptome_path,
    gtf_genome_path,
    counted_transcriptome_path,
):
    print("Sending to the counter genome queue...")

    app.send_task(
        "infrastructure.messaging.task.counter_transcriptome",
        args=(
            pipeline_id,
            sra_id,
            organism_group,
            aligned_transcriptome_path,
            gtf_genome_path,
            counted_transcriptome_path,
        ),
        queue="counter_transcriptome",
    )

    print("Message sent to the counter transcriptome queue!")


def diffed_transcriptome_task(pipeline_id, sra_files):

    print("Sending to the diffed transcriptome queue...")

    app.send_task(
        "infrastructure.messaging.task.generate_diferential_expression",
        args=(pipeline_id, sra_files),
        queue="generate_diferential_expression",
    )

    print("Message sent to the diffed transcriptome queue!")
