from datetime import datetime, time

def datetime_to_iso(dt):
    return dt.isoformat() if dt else None

def time_to_iso(t):
    return t.isoformat() if t else None

def parse_datetime_iso(s):
    if not s:
        return None
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    return dt.replace(tzinfo=None)
