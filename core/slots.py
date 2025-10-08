import uuid
from datetime import timedelta
import streamlit as st
from models import Slot

def add_slot_to_team(team_name, slot_type_name, client, start):
    slot_type = st.session_state["slot_types"][slot_type_name]
    new_slot = Slot(
        id=str(uuid.uuid4()),
        start=start,
        end=start + timedelta(minutes=slot_type.minutes),
        slot_type=slot_type_name,
        duration_min=slot_type.minutes,
        client=client
    )
    st.session_state["teams"][team_name].append(new_slot)
    return new_slot
