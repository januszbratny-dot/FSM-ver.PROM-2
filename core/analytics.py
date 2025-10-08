from datetime import timedelta
import streamlit as st

def get_total_usage():
    usage = {}
    for team_name, slots in st.session_state["teams"].items():
        total = sum(s.duration_min for s in slots)
        usage[team_name] = f"{total // 60}h {total % 60}min"
    return usage
