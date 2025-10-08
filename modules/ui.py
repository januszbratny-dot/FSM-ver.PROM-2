import streamlit as st
from modules.scheduler import weighted_choice, add_slot_to_brygada, get_day_slots_for_brygada
from modules.config import DEFAULT_WORK_START, DEFAULT_WORK_END, PREFERRED_SLOTS
from datetime import date, timedelta, datetime

def init_default_state():
    st.session_state.slot_types = [
        {"name": "Zlecenie krótkie", "minutes": 30, "weight": 1.0},
        {"name": "Zlecenie normalne", "minutes": 60, "weight": 1.0},
        {"name": "Zlecenie długie", "minutes": 90, "weight": 1.0}
    ]
    st.session_state.brygady = ["Brygada 1", "Brygada 2"]
    st.session_state.working_hours = {
        "Brygada 1": (DEFAULT_WORK_START, DEFAULT_WORK_END),
        "Brygada 2": (DEFAULT_WORK_START, DEFAULT_WORK_END)
    }
    st.session_state.schedules = {}
    st.session_state.clients_added = []
    st.session_state.client_counter = 1
    st.session_state.unscheduled_orders = []

def run_ui():
    st.title("📅 Harmonogram slotów - Tydzień")
    st.sidebar.subheader("⚙️ Konfiguracja")
    st.write("Wersja uproszczona UI dla modułów")

    # prosty booking
    today = date.today()
    client_name = st.text_input("Nazwa klienta", f"Klient {st.session_state.client_counter}")
    slot_type_name = st.selectbox("Typ slotu", [s["name"] for s in st.session_state.slot_types])
    if st.button("Zarezerwuj slot dziś"):
        slot_minutes = next(s["minutes"] for s in st.session_state.slot_types if s["name"] == slot_type_name)
        start_dt = datetime.combine(today, DEFAULT_WORK_START)
        end_dt = start_dt + timedelta(minutes=slot_minutes)
        add_slot_to_brygada(st.session_state.brygady[0], today, {
            "start": start_dt,
            "end": end_dt,
            "slot_type": slot_type_name,
            "duration_min": slot_minutes,
            "client": client_name
        })
        st.success(f"Zarezerwowano {slot_type_name} dla {client_name}")
        st.session_state.client_counter += 1
