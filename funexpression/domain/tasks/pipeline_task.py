from domain.entities.pipeline import Pipeline
from domain.tasks.genome.genome_download_task import GenomeDownloadTask
from domain.tasks.transcriptome.transcriptome_align_task import TranscripomeAlignTask
from domain.tasks.transcriptome.transcriptome_convert_task import (
    TranscripomeConvertTask,
)
from domain.tasks.transcriptome.transcriptome_download_task import (
    TranscriptomeDownloadTask,
)
from domain.tasks.transcriptome.transcriptome_trim import TranscriptomeTrimTask


class PipelineTask:
    def __init__(
        self,
        # genome_download_task: GenomeDownloadTask,
        # transtriptome_download_task: TranscriptomeDownloadTask,
        # transtriptome_convert_task: TranscripomeConvertTask,
        # transtriptome_trim_task: TranscriptomeTrimTask,
        transtriptome_align_task: TranscripomeAlignTask,
    ):
        # self.genome_download_task = genome_download_task
        # self.transtriptome_download_task = transtriptome_download_task
        # self.transtriptome_convert_task = transtriptome_convert_task
        # self.transcriptome_trim_task = transtriptome_trim_task
        self.transcriptome_align_task = transtriptome_align_task

    def start(self, pipeline: Pipeline):
        pass
        # return self.download_genome_and_transcriptome(pipeline)

    # def download_genome_and_transcriptome(self, pipeline: Pipeline):
    #     self.genome_download_task.download_genome(pipeline)
    #     self.transtriptome_download_task.download_transcriptomes(pipeline)

    #     return

    def aling_transcriptomes(self, pipeline: Pipeline):
        self.transcriptome_align_task.align_transcriptomes(pipeline)

        return
