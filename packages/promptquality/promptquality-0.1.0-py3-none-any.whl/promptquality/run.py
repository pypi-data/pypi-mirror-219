from pathlib import Path
from typing import Optional

from promptquality.get_metrics import get_metrics
from promptquality.helpers import (
    create_job,
    create_project,
    create_run,
    create_template,
    upload_dataset,
)
from promptquality.job_progress import job_progress
from promptquality.types.config import Config, set_config


def run(
    template: str,
    dataset: Path,
    project_name: Optional[str] = None,
    run_name: Optional[str] = None,
    template_name: Optional[str] = None,
) -> Config:
    config = set_config()
    # Create project.
    project_id = create_project(project_name, config)
    # Create template.
    template_version_id = create_template(
        template,
        project_id,
        template_name,
        config,
    )
    # Upload dataset.
    dataset_id = upload_dataset(
        dataset,
        project_id,
        template_version_id,
        config,
    )
    # Run prompt.
    run_id = create_run(
        project_id,
        run_name,
        config,
    )
    job_id = create_job(
        project_id,
        run_id,
        dataset_id,
        template_version_id,
        config,
    )
    job_progress(job_id, config)
    get_metrics(project_id=project_id, run_id=run_id, config=config)
    return config
