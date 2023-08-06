import logging
import sys

logger = logging.getLogger("arrlio")
logger.setLevel(logging.ERROR)

log_frmt = logging.Formatter("%(asctime)s %(levelname)8s %(name)27s lineno:%(lineno)4d -- %(message)s")
log_hndl = logging.StreamHandler(stream=sys.stderr)
log_hndl.setFormatter(log_frmt)
logger.addHandler(log_hndl)

# pylint: disable=wrong-import-position
from arrlio.core import App, AsyncResult, registered_tasks, task  # noqa
from arrlio.models import Graph, Task, TaskInstance, TaskResult  # noqa
from arrlio.settings import Config, TaskConfig  # noqa
