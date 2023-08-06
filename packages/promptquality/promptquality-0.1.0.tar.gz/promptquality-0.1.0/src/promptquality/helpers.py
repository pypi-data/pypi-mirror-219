from pathlib import Path
from typing import Optional

from pydantic import UUID4

from promptquality.types.config import Config, set_config
from promptquality.types.run import (
    CreateJobRequest,
    CreateJobResponse,
    CreateProjectRequest,
    CreateProjectResponse,
    CreateRunRequest,
    CreateRunResponse,
    CreateTemplateRequest,
    CreateTemplateResponse,
    GetJobStatusResponse,
    UploadDatasetRequest,
    UploadDatasetResponse,
)
from promptquality.utils.logger import logger


def create_project(
    project_name: Optional[str] = None, config: Optional[Config] = None
) -> UUID4:
    config = config or set_config()
    project_request = CreateProjectRequest(name=project_name)
    logger.debug(f"Creating project {project_request.name}...")
    response_dict = config.api_client.create_project(project_request)
    project_response = CreateProjectResponse.model_validate(response_dict)
    config.merge_project(project_response)
    logger.debug(
        f"Created project with name {project_response.name}, ID {project_response.id}."
    )
    return project_response.id


def create_template(
    template: str,
    project_id: UUID4,
    template_name: Optional[str] = None,
    config: Optional[Config] = None,
) -> UUID4:
    config = config or set_config()
    template_request = CreateTemplateRequest(
        template=template, project_id=project_id, name=template_name
    )
    logger.debug(f"Creating template {template_request.name}...")
    response_dict = config.api_client.create_template(template_request)
    template_response = CreateTemplateResponse.model_validate(response_dict)
    config.merge_template(template_response)
    logger.debug(
        f"Created template with name {template_response.name}, ID "
        f"{template_response.id}."
    )
    return template_response.selected_version_id


def upload_dataset(
    dataset: Path,
    project_id: UUID4,
    template_version_id: UUID4,
    config: Optional[Config] = None,
) -> UUID4:
    config = config or set_config()
    dataset_request = UploadDatasetRequest.from_dataset(
        dataset, project_id, template_version_id
    )
    logger.debug(f"Uploading dataset {dataset_request.file_path}...")
    response_dict = config.api_client.upload_dataset(dataset_request)
    dataset_response = UploadDatasetResponse.model_validate(response_dict)
    config.merge_dataset(dataset_response)
    logger.debug(f"Uploaded dataset with ID {dataset_response.id}.")
    return dataset_response.id


def create_run(
    project_id: UUID4, run_name: Optional[str] = None, config: Optional[Config] = None
) -> UUID4:
    config = config or set_config()
    run_request = CreateRunRequest(name=run_name, project_id=project_id)
    logger.debug(f"Creating run {run_request.name}...")
    response_dict = config.api_client.create_run(run_request)
    run_response = CreateRunResponse.model_validate(response_dict)
    config.merge_run(run_response)
    logger.debug(f"Created run with name {run_request.name}, ID {run_response.id}.")
    return run_response.id


def create_job(
    project_id: UUID4,
    run_id: UUID4,
    dataset_id: UUID4,
    template_version_id: UUID4,
    config: Optional[Config] = None,
) -> UUID4:
    config = config or set_config()
    job_request = CreateJobRequest(
        project_id=project_id,
        run_id=run_id,
        prompt_dataset_id=dataset_id,
        prompt_template_version_id=template_version_id,
    )
    logger.debug("Creating job...")
    response_dict = config.api_client.create_job(job_request)
    job_response = CreateJobResponse.model_validate(response_dict)
    config.merge_job(job_response)
    logger.debug(f"Created job with ID {job_response.id}.")
    return job_response.id


def get_job_status(
    job_id: Optional[UUID4] = None, config: Optional[Config] = None
) -> GetJobStatusResponse:
    config = config or set_config()
    logger.debug(f"Getting job status for job {job_id}...")
    job_id = job_id or config.current_job_id
    if not job_id:
        raise ValueError("job_id must be provided")
    response_dict = config.api_client.get_job_status(job_id)
    job_status_response = GetJobStatusResponse.model_validate(response_dict)
    logger.debug(
        f"Got job status for job {job_id}, status is "
        f"{job_status_response.progress_message}, "
        f"{job_status_response.progress_percent} percentage."
    )
    return job_status_response
