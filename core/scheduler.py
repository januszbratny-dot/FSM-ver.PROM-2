from datetime import datetime, timedelta
import random
import streamlit as st
from config import SEARCH_STEP_MINUTES
from core.slots import add_slot_to_team
from utils.time_utils import get_time_range

def schedule_client_immediately(client, slot_type_name, day, pref_start, pref_end):
    start, end = get_time_range(day, pref_start, pref_end)
    step = timedelta(minutes=SEARCH_STEP_MINUTES)

    for team_name, team_slots in st.session_state["teams"].items():
        current_time = start
        while current_time + timedelta(minutes=st.session_state["slot_types"][slot_type_name].minutes) <= end:
            if not any(s.start <= current_time < s.end for s in team_slots):
                slot = add_slot_to_team(team_name, slot_type_name, client, current_time)
                st.success(f"Zarezerwowano dla {client} w {team_name} o {current_time:%H:%M}")
                return slot
            current_time += step

    st.warning("Nie znaleziono dostępnego terminu.")
    return None
