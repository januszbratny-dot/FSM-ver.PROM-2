from datetime import datetime, time

def datetime_to_iso(dt: datetime) -> str:
    return dt.isoformat() if dt else None

def time_to_iso(t: time) -> str:
    return t.isoformat()

def parse_datetime_iso(s: str) -> datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    return dt.astimezone().replace(tzinfo=None) if dt.tzinfo else dt
