import json
import streamlit as st
from config import STORAGE_FILENAME
from utils.serialization import datetime_to_iso, parse_datetime_iso
from models import Slot, SlotType

def save_state_to_json():
    data = {
        "slot_types": {k: v.__dict__ for k, v in st.session_state.get("slot_types", {}).items()},
        "teams": {
            team: [slot.__dict__ | {"start": datetime_to_iso(slot.start), "end": datetime_to_iso(slot.end)}]
            for team, slots in st.session_state.get("teams", {}).items()
        }
    }
    with open(STORAGE_FILENAME, "w") as f:
        json.dump(data, f, indent=2)

def load_state_from_json():
    try:
        with open(STORAGE_FILENAME, "r") as f:
            data = json.load(f)
        st.session_state["slot_types"] = {k: SlotType(**v) for k, v in data["slot_types"].items()}
        st.session_state["teams"] = {
            team: [Slot(**{**s, "start": parse_datetime_iso(s["start"]), "end": parse_datetime_iso(s["end"])})
                   for s in slots]
            for team, slots in data["teams"].items()
        }
        st.session_state["initialized"] = True
    except FileNotFoundError:
        st.session_state["slot_types"] = {"Standard": SlotType("Standard", 60)}
        st.session_state["teams"] = {"Brygada 1": []}
        st.session_state["initialized"] = True
