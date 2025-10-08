import streamlit as st
from models import SlotType

def render_sidebar():
    st.sidebar.header("⚙️ Konfiguracja")
    with st.sidebar.expander("📦 Typy slotów"):
        name = st.text_input("Nazwa typu", "Standard")
        duration = st.number_input("Czas trwania (minuty)", 15, 240, 60)
        if st.button("➕ Dodaj typ"):
            st.session_state["slot_types"][name] = SlotType(name, duration)
            st.success(f"Dodano typ {name}")

    with st.sidebar.expander("👷‍♂️ Brygady"):
        new_team = st.text_input("Nowa brygada", "")
        if st.button("➕ Dodaj brygadę") and new_team:
            st.session_state["teams"][new_team] = []
            st.success(f"Dodano {new_team}")
