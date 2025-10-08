from datetime import time
import logging

STORAGE_FILENAME = "schedules.json"
SEARCH_STEP_MINUTES = 15
DEFAULT_WORK_START = time(8, 0)
DEFAULT_WORK_END = time(16, 0)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scheduler")
