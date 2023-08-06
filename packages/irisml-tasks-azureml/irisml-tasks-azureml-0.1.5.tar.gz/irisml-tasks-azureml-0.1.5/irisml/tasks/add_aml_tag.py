import dataclasses
import logging
from typing import Optional
from azureml.core import Run
import irisml.core


logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Tag the run with a string key and optional string value."""
    VERSION = "0.1.0"
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        tag: str
        value: Optional[str] = None

    def execute(self):
        try:
            run = Run.get_context(allow_offline=False)
            run.tag(self.config.tag, self.config.value)
        except Exception as e:
            logger.warning(f"{e}: Failed to tag the run.")
        return self.Outputs()

    def dry_run(self):
        self.execute()
