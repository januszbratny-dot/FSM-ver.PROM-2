from datetime import datetime, time

def parse_time_str(t: str) -> time:
    """Parsuje czas w formacie H:M, H:M:S, H:M:S.sss."""
    try:
        return time.fromisoformat(t)
    except Exception:
        from datetime import datetime as dt
        for fmt in ("%H:%M:%S.%f", "%H:%M:%S", "%H:%M"):
            try:
                return dt.strptime(t, fmt).time()
            except ValueError:
                continue
    raise ValueError(f"Nie można sparsować czasu: {t}")

def parse_datetime_iso(s: str):
    if s is None:
        return None
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is not None:
        dt = dt.astimezone().replace(tzinfo=None)
    return dt
