from getpass import getpass
from os import environ, getenv
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin
from webbrowser import open_new_tab

from pydantic import (
    UUID4,
    HttpUrl,
    SecretStr,
    ValidationError,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

from promptquality.constants.config import ConfigDefaults, ConfigEnvironmentVariables
from promptquality.constants.routes import Routes
from promptquality.types.run import (
    CreateJobResponse,
    CreateProjectResponse,
    CreatePromptTemplateVersionResponse,
    CreateRunResponse,
    CreateTemplateResponse,
    UploadDatasetResponse,
)
from promptquality.utils.api_client import ApiClient
from promptquality.utils.logger import logger


class Config(BaseSettings):
    console_url: HttpUrl
    # User.
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    token: Optional[SecretStr] = None
    current_user: Optional[str] = None
    # Project.
    current_project_id: Optional[UUID4] = None
    current_project_name: Optional[str] = None
    # Run.
    current_run_id: Optional[UUID4] = None
    current_run_name: Optional[str] = None
    # Template.
    current_template_id: Optional[UUID4] = None
    current_template_name: Optional[str] = None
    # Version
    current_template_version_id: Optional[UUID4] = None
    current_template_version: Optional[int] = None
    current_template: Optional[str] = None
    # Dataset.
    current_dataset_id: Optional[UUID4] = None
    # Job.
    current_job_id: Optional[UUID4] = None

    model_config = SettingsConfigDict(
        # Allow loading from environment variables.
        env_prefix="GALILEO_",
        # Ignore unknown fields when loading from a config file.
        extra="ignore",
        # Validate fields at assignment.
        validate_assignment=True,
    )

    @computed_field
    def api_url(self) -> HttpUrl:
        # Local dev.
        if self.console_url.host in ["localhost", "127.0.0.1"]:
            api_url = "http://localhost:8088"
        else:
            api_url = self.console_url.unicode_string().replace("console", "api")
        return HttpUrl(api_url)

    @property
    def config_file(self) -> Path:
        return _config_location()

    @field_validator("console_url", mode="before")
    def http_url(cls, value: str) -> str:
        if value and not (value.startswith("https") or value.startswith("http")):
            value = f"https://{value}"
        return value

    # Ignore arg-type until a fix for this issue is released:
    # https://github.com/pydantic/pydantic/issues/6709
    @model_validator(mode="after")  # type: ignore[arg-type]
    def validate_api_url(cls, config: "Config") -> "Config":
        if not ApiClient.healthcheck(str(config.api_url)):
            # TODO: Make this a custom error.
            raise ValidationError(f"Could not connect to {config.api_url}.")
        return config

    @field_serializer("token", when_used="json")
    def serialize_token(self, value: SecretStr) -> str:
        return value.get_secret_value()

    @classmethod
    def read(cls, config_directory: str = ConfigDefaults.config_directory) -> "Config":
        return cls.model_validate_json(
            Path.home()
            .joinpath(config_directory, ConfigDefaults.config_filename)
            .read_text()
        )

    def write(self) -> None:
        self.config_file.parent.mkdir(exist_ok=True)
        self.config_file.write_text(self.model_dump_json(exclude_none=True))

    @property
    def api_client(self) -> ApiClient:
        if not self.token:
            raise ValueError("No token set.")
        return ApiClient(api_url=self.api_url, token=self.token)

    def token_login(self) -> str:
        token_url = urljoin(str(self.console_url), Routes.get_token)
        logger.info(f"🔐 Opening {token_url} to generate a new API Key.")
        try:
            open_new_tab(token_url)
        except Exception:
            pass
        finally:
            print(f"Go to {token_url} to generate a new API Key")
            return getpass("🔐 Enter your API Key:")

    def login(self) -> None:
        if not self.token:
            token = (
                ApiClient.username_login(
                    str(self.api_url), self.username, str(self.password)
                ).get("access_token", "")
                if self.username and self.password
                else self.token_login()
            )
            self.token = SecretStr(token)
        self.current_user = self.api_client.get_current_user().get("email")
        self.write()
        print(
            f"👋 You have logged into 🔭 Galileo ({self.console_url}) as "
            f"{self.current_user}."
        )

    def logout(self) -> None:
        self.current_user = None
        self.token = None
        self.write()
        print("👋 You have logged out of 🔭 Galileo.")

    def merge_project(self, project: CreateProjectResponse) -> None:
        self.current_project_id = project.id
        self.current_project_name = project.name
        self.write()
        logger.debug(f"📝 Set current project to {project.name}.")

    def merge_template(self, template: CreateTemplateResponse) -> None:
        self.current_template_id = template.id
        self.current_template_name = template.name
        self.merge_template_version(template.selected_version)
        self.write()
        logger.debug(f"📝 Set current template to {template.name}.")

    def merge_template_version(
        self, template_version: CreatePromptTemplateVersionResponse
    ) -> None:
        self.current_template_version_id = template_version.id
        self.current_template_version = template_version.version
        self.current_template = template_version.template
        self.write()
        logger.debug(f"📝 Set current template version to {template_version.version}.")

    def merge_dataset(self, dataset: UploadDatasetResponse) -> None:
        self.current_dataset_id = dataset.id
        self.write()
        logger.debug(f"📝 Set current dataset to {dataset.id}.")

    def merge_run(self, run: CreateRunResponse) -> None:
        self.current_run_id = run.id
        self.current_run_name = run.name
        self.write()
        logger.debug(f"📝 Set current run to {run.name}.")

    def merge_job(self, job: CreateJobResponse) -> None:
        self.current_job_id = job.id
        self.write()
        logger.debug(f"📝 Set current job to {job.id}.")


def _config_location() -> Path:
    return Path.home().joinpath(
        ConfigDefaults.config_directory, ConfigDefaults.config_filename
    )


def set_config(console_url: Optional[str] = None) -> Config:
    if _config_location().exists():
        config = Config.read()
    elif console_url:
        config = Config(console_url=console_url)
    else:
        config = Config()
    config.write()
    return config


def set_console_url(console_url: Optional[str] = None) -> None:
    """For Enterprise users. Set the console URL to your Galileo Environment.

    You can also set GALILEO_CONSOLE_URL before importing promptquality to bypass this

    :param console_url: If set, that will be used. Otherwise, if an environment variable
    GALILEO_CONSOLE_URL is set, that will be used. Otherwise, you will be prompted for
    a url.
    """
    if not console_url:
        console_url = ConfigDefaults.console_url
    if getenv(ConfigEnvironmentVariables.console_url, None) is None:
        environ[ConfigEnvironmentVariables.console_url] = console_url
