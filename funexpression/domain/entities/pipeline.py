from dataclasses import dataclass
from typing import Optional
from domain.entities.pipeline_stage_enum import PipelineStageEnum
from domain.entities.triplicate import SRAFile, SRAFileStatusEnum, Triplicate


@dataclass
class Pipeline:
    run_id: str
    email: str
    stage: PipelineStageEnum
    control_organism: Triplicate
    experiment_organism: Triplicate
    reference_genome_acession_number: str
    id: Optional[int] = None

    def to_json(self):
        return {
            "id": str(self.id),
            "run_id": self.run_id,
            "email": self.email,
            "stage": self.stage.value,
            "control_organism": {
                "srr_1": {
                    "acession_number": self.control_organism.srr_1.acession_number,
                    "status": self.control_organism.srr_1.status.value,
                },
                "srr_2": {
                    "acession_number": self.control_organism.srr_2.acession_number,
                    "status": self.control_organism.srr_2.status.value,
                },
                "srr_3": {
                    "acession_number": self.control_organism.srr_3.acession_number,
                    "status": self.control_organism.srr_3.status.value,
                },
            },
            "experiment_organism": {
                "srr_1": {
                    "acession_number": self.experiment_organism.srr_1.acession_number,
                    "status": self.experiment_organism.srr_1.status.value,
                },
                "srr_2": {
                    "acession_number": self.experiment_organism.srr_2.acession_number,
                    "status": self.experiment_organism.srr_2.status.value,
                },
                "srr_3": {
                    "acession_number": self.experiment_organism.srr_3.acession_number,
                    "status": self.experiment_organism.srr_3.status.value,
                },
            },
            "reference_genome_acession_number": self.reference_genome_acession_number,
        }

    @staticmethod
    def from_json(json: dict):
        return Pipeline(
            id=str(json["_id"]),
            run_id=json["run_id"],
            email=json["email"],
            stage=PipelineStageEnum(json["stage"]),
            control_organism=Triplicate(
                srr_1=SRAFile(
                    acession_number=json["control_organism"]["srr_1"][
                        "acession_number"
                    ],
                    status=SRAFileStatusEnum[
                        json["control_organism"]["srr_1"]["status"]
                    ],
                ),
                srr_2=SRAFile(
                    acession_number=json["control_organism"]["srr_2"][
                        "acession_number"
                    ],
                    status=SRAFileStatusEnum[
                        json["control_organism"]["srr_2"]["status"]
                    ],
                ),
                srr_3=SRAFile(
                    acession_number=json["control_organism"]["srr_3"][
                        "acession_number"
                    ],
                    status=SRAFileStatusEnum[
                        json["control_organism"]["srr_3"]["status"]
                    ],
                ),
            ),
            experiment_organism=Triplicate(
                srr_1=SRAFile(
                    acession_number=json["experiment_organism"]["srr_1"][
                        "acession_number"
                    ],
                    status=SRAFileStatusEnum[
                        json["experiment_organism"]["srr_1"]["status"]
                    ],
                ),
                srr_2=SRAFile(
                    acession_number=json["experiment_organism"]["srr_2"][
                        "acession_number"
                    ],
                    status=SRAFileStatusEnum[
                        json["experiment_organism"]["srr_2"]["status"]
                    ],
                ),
                srr_3=SRAFile(
                    acession_number=json["experiment_organism"]["srr_3"][
                        "acession_number"
                    ],
                    status=SRAFileStatusEnum[
                        json["experiment_organism"]["srr_3"]["status"]
                    ],
                ),
            ),
            reference_genome_acession_number=json["reference_genome_acession_number"],
        )
