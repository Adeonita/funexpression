from domain.entities.pipeline import Pipeline

class PipelineTask:

    #TODO: usar instancia das tasks de cada classe
    def _download_genome_and_transcriptome(self, pipeline: Pipeline):
        self._download_genome(pipeline)
        self._download_transcriptomes(pipeline)

        return

   





