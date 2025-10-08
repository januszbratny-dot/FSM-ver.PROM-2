from core.slots import add_slot_to_team
from models import SlotType
from datetime import datetime
import streamlit as st

def test_add_slot_creates_valid_slot():
    st.session_state["slot_types"] = {"Standard": SlotType("Standard", 60)}
    st.session_state["teams"] = {"Brygada 1": []}
    slot = add_slot_to_team("Brygada 1", "Standard", "Test Client", datetime(2025, 10, 8, 8, 0))
    assert slot.duration_min == 60
    assert slot.client == "Test Client"
