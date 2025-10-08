from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SlotType:
    name: str
    minutes: int
    weight: float = 1.0

@dataclass
class Slot:
    id: str
    start: datetime
    end: datetime
    slot_type: str
    duration_min: int
    client: str
    pref_range: Optional[str] = None
