import os, json, tempfile
import uuid, logging
import streamlit as st
from modules.utils import parse_datetime_iso, parse_time_str
from modules.config import DEFAULT_WORK_START, DEFAULT_WORK_END

logger = logging.getLogger("scheduler")

def _datetime_to_iso(dt):
    return dt.isoformat() if dt else None

def _time_to_iso(t):
    return t.isoformat() if t else None

def schedules_to_jsonable():
    data = {}
    for b, days in st.session_state.schedules.items():
        data[b] = {}
        for d, slots in days.items():
            data[b][d] = [
                {
                    "id": s.get("id"),
                    "start": _datetime_to_iso(s["start"]),
                    "end": _datetime_to_iso(s["end"]),
                    "slot_type": s["slot_type"],
                    "duration_min": s["duration_min"],
                    "client": s["client"],
                    "pref_range": s.get("pref_range"),
                }
                for s in slots
            ]
    return {
        "slot_types": st.session_state.slot_types,
        "brygady": st.session_state.brygady,
        "working_hours": {
            b: (_time_to_iso(wh[0]), _time_to_iso(wh[1]))
            for b, wh in st.session_state.working_hours.items()
        },
        "schedules": data,
        "clients_added": st.session_state.clients_added,
        "client_counter": st.session_state.client_counter,
        "unscheduled_orders": st.session_state.get("unscheduled_orders", []),
    }

def save_state_to_json(filename="schedules.json"):
    data = schedules_to_jsonable()
    dirn = os.path.dirname(os.path.abspath(filename)) or "."
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=dirn, delete=False) as tf:
        json.dump(data, tf, ensure_ascii=False, indent=2)
        tmpname = tf.name
    os.replace(tmpname, filename)
    logger.info(f"State saved to {filename}")

def load_state_from_json(filename="schedules.json") -> bool:
    if not os.path.exists(filename):
        return False
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        logger.exception("Nie udało się wczytać JSON. Tworzę świeży stan.")
        return False

    st.session_state.slot_types = data.get("slot_types", [])
    st.session_state.brygady = data.get("brygady", [])
    st.session_state.working_hours = {}
    for b, wh in data.get("working_hours", {}).items():
        try:
            st.session_state.working_hours[b] = (parse_time_str(wh[0]), parse_time_str(wh[1]))
        except Exception:
            st.session_state.working_hours[b] = (DEFAULT_WORK_START, DEFAULT_WORK_END)

    st.session_state.schedules = {}
    for b, days in data.get("schedules", {}).items():
        st.session_state.schedules[b] = {}
        for d, slots in days.items():
            st.session_state.schedules[b][d] = [
                {
                    "id": s.get("id", str(uuid.uuid4())),
                    "start": parse_datetime_iso(s.get("start")),
                    "end": parse_datetime_iso(s.get("end")),
                    "slot_type": s.get("slot_type"),
                    "duration_min": s.get("duration_min"),
                    "client": s.get("client"),
                    "pref_range": s.get("pref_range"),
                }
                for s in slots
            ]
    st.session_state.clients_added = data.get("clients_added", [])
    st.session_state.client_counter = data.get("client_counter", 1)
    st.session_state.unscheduled_orders = data.get("unscheduled_orders", [])
    return True
