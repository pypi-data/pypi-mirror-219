from types import SimpleNamespace

# We cannot use Enum here because `mypy` doesn't like it when we format those routes
# into strings. https://github.com/python/mypy/issues/15269
Routes = SimpleNamespace(
    healthcheck="healthcheck",
    login="login",
    get_token="get-token",
    current_user="current_user",
    projects="projects",
    templates="projects/{project_id}/templates",
    dataset="projects/{project_id}/upload_prompt_dataset",
    runs="projects/{project_id}/runs",
    jobs="jobs",
    metrics="projects/{project_id}/runs/{run_id}/metrics",
)
