from datetime import time

STORAGE_FILENAME = "schedules.json"
SEARCH_STEP_MINUTES = 15
DEFAULT_WORK_START = time(8, 0)
DEFAULT_WORK_END = time(16, 0)

# Przykładowe preferowane sloty
PREFERRED_SLOTS = {
    "8:00-11:00": (time(8, 0), time(11, 0)),
    "11:00-14:00": (time(11, 0), time(14, 0)),
    "14:00-17:00": (time(14, 0), time(17, 0)),
    "17:00-20:00": (time(17, 0), time(20, 0)),
}
