def log_processing_queue_error_message(
    sra_id: str, pipeline_stage: str, error: Exception
):
    return f"re-enqueue {sra_id} to {pipeline_stage} queue, because ocurred an error: {error}"
