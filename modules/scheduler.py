import random
import uuid
from datetime import datetime, timedelta
import streamlit as st
from modules.utils import parse_time_str
from modules.config import DEFAULT_WORK_START, DEFAULT_WORK_END, SEARCH_STEP_MINUTES

def weighted_choice(slot_types):
    if not slot_types:
        return None
    names = [s["name"] for s in slot_types]
    weights = [s.get("weight", 1) for s in slot_types]
    return random.choices(names, weights=weights, k=1)[0]

def _wh_minutes(wh_start, wh_end):
    start_dt = datetime.combine(datetime.today(), wh_start)
    end_dt = datetime.combine(datetime.today(), wh_end)
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)
    return int((end_dt - start_dt).total_seconds() // 60)

def get_day_slots_for_brygada(brygada, day):
    d = day.strftime("%Y-%m-%d")
    return sorted(st.session_state.schedules.get(brygada, {}).get(d, []), key=lambda s: s["start"])

def add_slot_to_brygada(brygada, day, slot, save=True):
    s = dict(slot)
    if "id" not in s:
        s["id"] = str(uuid.uuid4())
    d = day.strftime("%Y-%m-%d")
    st.session_state.schedules.setdefault(brygada, {})
    st.session_state.schedules[brygada].setdefault(d, [])
    # prosty mechanizm przyjazdu
    s["arrival_window_start"] = s["start"]
    s["arrival_window_end"] = s["end"]
    existing = st.session_state.schedules[brygada][d]
    overlap = any(not (s["end"] <= s_exist["start"] or s["start"] >= s_exist["end"]) for s_exist in existing)
    if overlap:
        return False
    st.session_state.schedules[brygada][d].append(s)
    st.session_state.schedules[brygada][d].sort(key=lambda x: x["start"])
    if save:
        from modules.persistence import save_state_to_json
        save_state_to_json()
    return True
