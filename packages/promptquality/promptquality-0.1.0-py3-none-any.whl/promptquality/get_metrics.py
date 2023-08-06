from typing import Optional

from pydantic import UUID4

from promptquality.types.config import Config, set_config
from promptquality.types.run import GetMetricsRequest, PromptMetrics


def get_metrics(
    project_id: Optional[UUID4] = None,
    run_id: Optional[UUID4] = None,
    config: Optional[Config] = None,
) -> PromptMetrics:
    config = config or set_config()
    project_id = project_id or config.current_project_id
    run_id = run_id or config.current_run_id
    if not project_id:
        raise ValueError("project_id must be provided")
    if not run_id:
        raise ValueError("run_id must be provided")
    metrics_request = GetMetricsRequest(project_id=project_id, run_id=run_id)
    all_metrics = config.api_client.get_metrics(metrics_request)
    return PromptMetrics.model_validate(all_metrics[-1]["extra"])
