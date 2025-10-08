import streamlit as st
from datetime import date, time
from core.scheduler import schedule_client_immediately

def render_booking_ui():
    st.subheader("🧾 Nowa rezerwacja")
    client = st.text_input("Klient")
    slot_type_name = st.selectbox("Rodzaj usługi", list(st.session_state["slot_types"].keys()))
    day = st.date_input("Dzień", value=date.today())
    pref_start = st.time_input("Preferowany początek", value=time(8, 0))
    pref_end = st.time_input("Preferowany koniec", value=time(16, 0))
    if st.button("📅 Zarezerwuj"):
        schedule_client_immediately(client, slot_type_name, day, pref_start, pref_end)
