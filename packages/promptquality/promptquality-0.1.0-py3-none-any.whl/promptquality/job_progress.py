from math import exp
from time import sleep
from typing import Optional

from pydantic import UUID4
from tqdm.auto import tqdm

from promptquality.constants.run import RunDefaults
from promptquality.helpers import get_job_status
from promptquality.types.config import Config


def job_progress(
    job_id: Optional[UUID4] = None, config: Optional[Config] = None
) -> UUID4:
    backoff = 0.5
    job_status = get_job_status(job_id, config)
    job_progress_bar = tqdm(
        total=job_status.steps_total,
        position=0,
        leave=True,
        desc=job_status.progress_message,
    )
    while job_status.status == RunDefaults.job_in_progress:
        job_status = get_job_status(job_id, config)
        job_progress_bar.set_description(job_status.progress_message)
        job_progress_bar.update(job_status.steps_completed - job_progress_bar.n)
        sleep(backoff)
        backoff = exp(backoff)
    job_progress_bar.close()
    if job_status.status == RunDefaults.job_failed:
        raise ValueError("Job failed.")
    return job_status.id
