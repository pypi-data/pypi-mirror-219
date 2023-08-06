from io import BufferedReader
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import UUID4, BaseModel, Field, field_validator

from promptquality.constants.run import RunDefaults
from promptquality.utils.name import random_name


class RandomName(BaseModel):
    name: str = Field(default_factory=random_name)

    @field_validator("name", mode="before")
    def set_name(cls, value: Optional[str]) -> str:
        if value is None:
            return random_name()
        return value


class CreateProjectRequest(RandomName):
    type: str = RunDefaults.project_type


class CreateProjectResponse(CreateProjectRequest):
    id: UUID4


class CreateTemplateRequest(RandomName):
    template: str
    project_id: UUID4


class CreatePromptTemplateVersionResponse(BaseModel):
    id: UUID4
    template: str
    version: int


class CreateTemplateResponse(RandomName):
    id: UUID4
    template: str
    selected_version: CreatePromptTemplateVersionResponse
    selected_version_id: UUID4
    all_versions: List[CreatePromptTemplateVersionResponse] = Field(
        default_factory=list
    )


class UploadDatasetRequest(BaseModel):
    project_id: UUID4
    file_path: Path
    prompt_template_version_id: UUID4

    @classmethod
    def from_dataset(
        cls, dataset: Path, project_id: UUID4, template_version_id: UUID4
    ) -> "UploadDatasetRequest":
        return cls(
            project_id=project_id,
            file_path=dataset,
            prompt_template_version_id=template_version_id,
        )

    @property
    def data(self) -> Dict[str, str]:
        return dict(prompt_template_version_id=str(self.prompt_template_version_id))

    @property
    def files(self) -> Dict[str, BufferedReader]:
        return dict(file=self.file_path.open("rb"))


class UploadDatasetResponse(BaseModel):
    id: UUID4 = Field(alias="dataset_id")


class CreateRunRequest(RandomName):
    project_id: UUID4
    task_type: int = RunDefaults.task_type


class CreateRunResponse(CreateRunRequest):
    id: UUID4


class CreateJobRequest(BaseModel):
    project_id: UUID4
    run_id: UUID4
    prompt_dataset_id: UUID4
    prompt_template_version_id: UUID4
    job_name: str = RunDefaults.job_name
    task_type: int = RunDefaults.task_type


class CreateJobResponse(CreateJobRequest):
    id: UUID4 = Field(alias="job_id")


class GetMetricsRequest(BaseModel):
    project_id: UUID4
    run_id: UUID4


class PromptMetrics(BaseModel):
    total_responses: Optional[int] = None
    average_hallucination: Optional[float] = None
    average_bleu: Optional[float] = None
    average_rouge: Optional[float] = None
    average_cost: Optional[float] = None
    total_cost: Optional[float] = None


class GetJobStatusResponse(BaseModel):
    id: UUID4
    project_id: UUID4
    run_id: UUID4
    status: str
    error_message: Optional[str]
    progress_message: Optional[str]
    steps_completed: int = 0
    steps_total: int = 0
    progress_percent: float = 0.0
